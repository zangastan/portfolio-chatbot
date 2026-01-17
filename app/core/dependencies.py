from typing import Generator, Annotated, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from supabase import Client

from app.core.database import supabase
from app.core.security import decode_access_token
from fastapi.security import APIKeyHeader
from app.services.api_key_service import APIKeyService
from app.models.api_key import APIKey

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

def get_db() -> Client:
    """
    Returns the Supabase client.
    """
    return supabase

async def get_current_api_key(
    key: str = Depends(api_key_header)
) -> APIKey:
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-KEY header"
        )
    
    service = APIKeyService()
    api_key_obj = service.validate_key(key)
    
    if not api_key_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API Key"
        )
    return api_key_obj

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Verify token via Supabase API (handles ES256/RS256/HS256 automatically)
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise credentials_exception
        return user_response.user
    except Exception as e:
        print(f"DEBUG: Authorization failed. Supabase API Error: {e}")
        raise credentials_exception

def get_current_tenant(current_user: Annotated[Any, Depends(get_current_user)]) -> str:
    """
    Extracts the tenant_id from the user's metadata or DB fallback.
    """
    # 1. Try metadata first (fastest)
    app_metadata = current_user.app_metadata or {}
    tenant_id = app_metadata.get("tenant_id")
    print(tenant_id)
    if not tenant_id:
        user_metadata = current_user.user_metadata or {}
        tenant_id = user_metadata.get("tenant_id")

    # 2. Fallback to DB if metadata is missing (e.g. newly created user)
    if not tenant_id:
        print(f"DEBUG: tenant_id missing in JWT for user {current_user.id}. Checking DB...")
        try:
            user_id = str(current_user.id)
            user_resp = supabase.table("users").select("tenant_id").eq("id", user_id).execute()
            if user_resp.data:
                tenant_id = user_resp.data[0].get("tenant_id")
                print(f"DEBUG: Found tenant_id {tenant_id} in DB.")
        except Exception as e:
            print(f"DEBUG: DB Fallback failed: {e}")

    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant ID not found for user. Please ensure you are assigned to a tenant."
        )
    # Ensure tenant_id is simplified to string if it's UUID
    return str(tenant_id)
