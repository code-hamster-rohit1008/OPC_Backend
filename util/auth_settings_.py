from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
import os

class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "1f9f50825a06f9cb6a175b92ba8f121f")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/sign-in")