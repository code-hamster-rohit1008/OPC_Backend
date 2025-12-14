from model.auth import Otp, UserInfo, UserCreds, GoogleToken, ForgotPasswordRequest, groom
from util.email_ import generate_otp, send_email_async
from util.emails_template_ import otp_format_signin, otp_format_signup, signup_confirmation_email, password_reset_email
from util.tokens_ import create_access_token, create_refresh_token
from util.hash_ import get_password_hash, verify_password
from util.authorization_ import get_current_user
from util.auth_settings_ import settings, oauth2_scheme
from db.rules import add, get, get_all, update, delete
from fastapi import APIRouter, Depends
from google.auth.transport import requests as google_auth_requests
from google.oauth2 import id_token
from datetime import datetime, timedelta, timezone
from bson import ObjectId
import jwt
import hashlib, os
from fastapi import BackgroundTasks

router = APIRouter()

@router.post('/sign-up')
async def sign_up(user: UserInfo, background_tasks: BackgroundTasks):
    try:
        user_data = groom(user.model_dump())
        
        if 'password' in user_data:
            user_data['password'] = await get_password_hash(user_data['password'])

        existing_perm_user = get({'user_type': user_data['user_type'], 'email': user_data['email']}, 'PERM_USERS', 'USERS')
        if existing_perm_user:
            return {'status_code': 400, 'message': 'User already exists. Please sign in instead.'}
        
        OTP = await generate_otp()
        try:
            email_content = await otp_format_signup(user_data['user_name'], OTP)
            background_tasks.add_task(send_email_async, user_data['email'], os.getenv('SMTP_USER'), email_content['subject_'], email_content['body_'])
        except Exception as e:
            return {'status_code': 500, 'message': 'Failed to send OTP email, please try again.', 'error': str(e)}
        
        user_data['otp'] = hashlib.sha256(OTP.encode()).hexdigest()

        update(
            {'user_type': user_data['user_type'], 'email': user_data['email']}, 
            user_data, 
            'TEMP_USERS', 
            'USERS', 
            {'upsert': True}
        )
        return {'status_code': 200, 'message': 'OTP sent to your email successfully'}

    except Exception as e:
        print(f"Sign-up Error: {e}")
        return {'status_code': 500, 'message': 'Error during sign up, please try again later.'}


@router.post('/sign-in')
async def sign_in(user: UserCreds, background_tasks: BackgroundTasks):
    try:
        user_data = groom(user.model_dump())
        
        existing_perm_user = get({'email': user_data['email']}, 'PERM_USERS', 'USERS')
        
        if not existing_perm_user:
            return {'status_code': 400, 'message': 'User does not exist, please sign up first.'}
        
        if not await verify_password(user_data['password'], existing_perm_user['password']):
            return {'status_code': 400, 'message': 'Invalid credentials.'}

        OTP = await generate_otp()
        try:
            email_content = await otp_format_signin(existing_perm_user['user_name'], OTP)
            background_tasks.add_task(send_email_async, user_data['email'], os.getenv('SMTP_USER'), email_content['subject_'], email_content['body_'])
        except Exception:
            return {'status_code': 500, 'message': 'Failed to send OTP email, please try again.'}
        
        temp_data = {
            'email': user_data['email'],
            'otp': hashlib.sha256(OTP.encode()).hexdigest(),
            'login_flow': True,
            'created_at': datetime.now(timezone.utc)
        }

        update(
            {'email': user_data['email'], 'login_flow': True}, 
            temp_data, 
            'TEMP_USERS', 
            'USERS', 
            {'upsert': True}
        )
        return {'status_code': 200, 'message': 'OTP sent to your email successfully'}

    except Exception as e:
        print(f"Sign-in Error: {e}")
        return {'status_code': 500, 'message': 'Error during sign in, please try again later.'}


@router.post('/verify-otp')
async def verify_otp(otp: Otp, background_tasks: BackgroundTasks):
    try:
        otp_hashed = hashlib.sha256(otp.otp.encode()).hexdigest()
        temp_user = get({'otp': otp_hashed}, 'TEMP_USERS', 'USERS')
        
        if not temp_user:
            return {'status_code': 400, 'message': 'Invalid or expired OTP, please try again.'}

        if temp_user.get('reset_flow'):
            hashed_password = await get_password_hash(temp_user['new_password'])
            update(
                {'email': temp_user['email']},
                {'password': hashed_password, 'last_logout_time': datetime.now(timezone.utc)}, 
                'PERM_USERS',
                'USERS',
                {'upsert': False}
            )
            delete({'email': temp_user['email'], 'otp': otp_hashed, 'reset_flow': True}, 'TEMP_USERS', 'USERS')
            return {'status_code': 200, 'message': 'Password updated successfully. Please sign in again.'}

        user_id, message = None, ""

        if temp_user.get('user_type'):
            temp_user.pop('_id')
            temp_user.pop('otp')
            new_user = add(temp_user, 'PERM_USERS', 'USERS')
            delete({'email': temp_user['email'], 'user_type': temp_user['user_type']}, 'TEMP_USERS', 'USERS')
            
            if new_user:
                user_id = str(new_user)
            else:
                saved_user = get({'email': temp_user['email']}, 'PERM_USERS', 'USERS')
                user_id = str(saved_user['_id'])
            email_content = await signup_confirmation_email(temp_user['user_name'])
            background_tasks.add_task(send_email_async, to_=temp_user['email'], from_=os.getenv("SMTP_USER"), subject_=email_content['subject_'], body_=email_content['body_'])
            message = 'OTP verified successfully, user registered.'

        elif temp_user.get('login_flow'):
            perm_user = get({'email': temp_user['email']}, 'PERM_USERS', 'USERS')
            if not perm_user:
                return {'status_code': 400, 'message': 'User record missing.'}
            user_id = str(perm_user['_id'])
            delete({'email': temp_user['email'], 'login_flow': True}, 'TEMP_USERS', 'USERS')
            message = 'OTP verified successfully, user signed in.'
        else:
            return {'status_code': 400, 'message': 'Invalid OTP context.'}

        if user_id:
            access_token = await create_access_token(data={"sub": user_id})
            refresh_token = await create_refresh_token(data={"sub": user_id})
            
            return {
                'status_code': 200, 
                'message': message,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer'
            }
        else:
            return {'status_code': 500, 'message': 'Could not retrieve user ID.'}

    except Exception as e:
        print(f"Verify OTP Error: {e}")
        return {'status_code': 500, 'message': 'Error during OTP verification.'}


@router.post('/google-sign-in')
async def google_sign_in(token_info: GoogleToken):
    try:
        try:
            id_info = id_token.verify_oauth2_token(
                token_info.google_id_token, 
                google_auth_requests.Request(), 
                os.getenv('GOOGLE_CLIENT_ID')
            )
        except Exception as e:
            return {'status_code': 400, 'message': f'Invalid Google ID token'}

        email = id_info['email']
        existing_perm_user = get({'email': email}, 'PERM_USERS', 'USERS')
        
        user_id, message = None, ""

        if existing_perm_user:
            user_id = str(existing_perm_user['_id'])
            message = 'User signed in successfully'
        else:
            return {'status_code': 400, 'message': 'User does not exist, please sign up first.'}

        access_token = await create_access_token(data={"sub": user_id})
        refresh_token = await create_refresh_token(data={"sub": user_id})

        return {
            'status_code': 200, 
            'message': message,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'
        }

    except Exception as e:
        print(f"Google Sign-In Error: {e}")
        return {'status_code': 500, 'message': 'Error during Google sign in.'}


@router.post('/logout')
async def logout(user_id: str = Depends(get_current_user)):
    try:
        if not user_id:
            return {'status_code': 401, 'message': 'Invalid token.'}
        
        try:
            uid_query = {'_id': ObjectId(user_id)}
        except:
            uid_query = {'_id': user_id}

        update(
            uid_query, 
            {'last_logout_time': datetime.now(timezone.utc)},
            'PERM_USERS',
            'USERS',
            {'upsert': False}
        )
        return {'status_code': 200, 'message': 'Logged out successfully'}
    except Exception as e:
        print(f"Logout Error: {e}")
        return {'status_code': 500, 'message': 'Error during logout.'}


@router.post('/forgot-password')
async def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks):
    try:
        email = request.email
        user = get({'email': email}, 'PERM_USERS', 'USERS')
        if not user:
            return {'status_code': 404, 'message': 'User not found.'}

        OTP = await generate_otp()
        try:
            email_content = await password_reset_email(user['user_name'], OTP)
            background_tasks.add_task(send_email_async, email, os.getenv('SMTP_USER'), email_content['subject_'], email_content['body_'])
        except Exception:
            return {'status_code': 500, 'message': 'Failed to send OTP email.'}

        temp_data = {
            'email': email,
            'new_password': request.new_password,
            'otp': hashlib.sha256(OTP.encode()).hexdigest(),
            'reset_flow': True,
            'created_at': datetime.now(timezone.utc)
        }
        update(
            {'email': email, 'reset_flow': True}, 
            temp_data, 
            'TEMP_USERS', 
            'USERS', 
            {'upsert': True}
        )
        return {'status_code': 200, 'message': 'Password reset OTP sent.'}

    except Exception as e:
        print(f"Forgot Password Error: {e}")
        return {'status_code': 500, 'message': 'Error processing request.'}


@router.post('/refresh')
async def refresh_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_iat = payload.get("iat")
        
        if user_id is None:
            return {'status_code': 401, 'message': "Invalid refresh token"}

        try:
            user = get({'_id': ObjectId(user_id)}, 'PERM_USERS', 'USERS')
        except:
            user = get({'_id': user_id}, 'PERM_USERS', 'USERS')
        
        if user is None:
            return {'status_code': 404, 'message': "User not found."}

        if user.get("last_logout_time"):
            last_logout = user["last_logout_time"]
            if last_logout.tzinfo is None:
                last_logout = last_logout.replace(tzinfo=timezone.utc)
            token_issued_at = datetime.fromtimestamp(token_iat, tz=timezone.utc)
            
            if token_issued_at < last_logout - timedelta(seconds=1):
                return {'status_code': 403, 'message': "Refresh token revoked (user logged out). Please sign in again."}
        
        new_access_token = await create_access_token(data={"sub": user_id})
        return {
            "status_code": 200,
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        print(f"Refresh Error: {e}")
        return {'status_code': 500, 'message': "Error refreshing token."}
    

@router.get('/me')
async def get_current_user_info(user_id: str = Depends(get_current_user)):
    try:
        if user_id is None:
            return {'status_code': 401, 'message': 'Invalid token.'}
        
        try:
            user = get({'_id': ObjectId(user_id)}, 'PERM_USERS', 'USERS')
        except:
            user = get({'_id': user_id}, 'PERM_USERS', 'USERS')
            
        if user is None:
             return {'status_code': 404, 'message': 'User not found.'}

        user.pop('password', None)
        if '_id' in user:
            user['_id'] = str(user['_id'])
        
        if 'created_at' in user and isinstance(user['created_at'], datetime):
            user['created_at'] = user['created_at'].isoformat()
        if 'last_logout_time' in user and isinstance(user['last_logout_time'], datetime):
            user['last_logout_time'] = user['last_logout_time'].isoformat()

        return {
            'status_code': 200, 
            'message': 'Token is valid.',
            'user': user
        }
    except Exception as e:
        print(f"Me Endpoint Error: {e}")
        return {'status_code': 500, 'message': 'Error fetching user info.'}

@router.get('/all_user_types')
async def get_all_user_types(user_id: str = Depends(get_current_user)):
    try:
        if user_id is None:
            return {'status_code': 401, 'message': 'Invalid token.'}
        
        email = get({'_id': ObjectId(user_id)}, 'PERM_USERS', 'USERS')['email']
        accounts = get_all({'email': email}, 'PERM_USERS', 'USERS')
        user_types = []
        for account in accounts:
            user_types.append(account['user_type'])
        return {'status_code': 200, 'message': 'User types fetched successfully', 'user_types': user_types}
    except Exception as e:
        print(f"All User Types Error: {e}")
        return {'status_code': 500, 'message': 'Error fetching user types.'}