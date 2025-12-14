from pydantic import BaseModel

class UserInfo(BaseModel):
    user_type: str
    user_name: str
    email: str
    phone_number: int
    password: str

class UserCreds(BaseModel):
    email: str
    password: str

class Otp(BaseModel):
    otp: str

class GoogleToken(BaseModel):
    google_id_token: str

class ForgotPasswordRequest(BaseModel):
    email: str
    new_password: str

def groom(data: dict) -> dict:
    not_null_data = {k: v for k, v in data.items() if v not in [None, "", 0]}
    structured_data = {k: v.lower() if isinstance(v, str) and k not in ['password', 'user_name'] else v for k, v in not_null_data.items()}
    return structured_data