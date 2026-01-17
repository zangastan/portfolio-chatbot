from datetime import datetime, timedelta
from typing import Optional, Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password[:72])

def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decodes the JWT token using the proper secret.
    Raises jwt.JWTError if invalid.
    """
    try:
        header = jwt.get_unverified_header(token)
        print(f"DEBUG: Token Header: {header}")
        return jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=[ALGORITHM, "RS256"], options={"verify_aud": False})
    except Exception as e:
        print(f"DEBUG: Token decode failed: {e}")
        raise e
