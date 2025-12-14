from db.rules import get
from util.auth_settings_ import settings, oauth2_scheme
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from bson import ObjectId
import jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_iat = payload.get("iat")
        
        if not user_id:
            return None
            
    except Exception as e:
        return None

    try:
        user = get({'_id': ObjectId(user_id)}, 'PERM_USERS', 'USERS')
    except:
        user = get({'_id': user_id}, 'PERM_USERS', 'USERS')

    if user is None:
        return None

    if user.get("last_logout_time"):
        last_logout = user["last_logout_time"]
        if last_logout.tzinfo is None:
            last_logout = last_logout.replace(tzinfo=timezone.utc)
        token_issued_at = datetime.fromtimestamp(token_iat, tz=timezone.utc)
        
        if token_issued_at < last_logout - timedelta(seconds=1):
            return None

    return user_id
