from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.api_key import APIKeyRequest, APIKeyResponse, APIKeyCreateResponse
from app.services.api_key_service import APIKeyService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
service = APIKeyService()

@router.post("/", response_model=APIKeyCreateResponse)
def create_api_key(
    request: APIKeyRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new API key. The secret key is returned strictly once.
    """
    api_key, secret = service.create_key(
        user_id=str(current_user.id),
        name=request.name,
        scopes=request.scopes
    )
    
    # Manually construct response to include secret
    response = APIKeyCreateResponse(
        id=api_key.id,
        name=api_key.name,
        prefix=api_key.prefix,
        scopes=api_key.scopes,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        last_used_at=api_key.last_used_at,
        secret_key=secret
    )
    return response

@router.get("/", response_model=List[APIKeyResponse])
def list_api_keys(
    current_user: User = Depends(get_current_user)
):
    """
    List all API keys belonging to the current user.
    """
    return service.list_keys(user_id=str(current_user.id))

@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    key_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Revoke an API key.
    """
    success = service.revoke_key(key_id, str(current_user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API Key not found or does not belong to you"
        )
