from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any
from app.services.auth_service import AuthService
from app.models.user import UserCreate
router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Adapt form data to service expected dict
        return auth_service.login({"email": form_data.username, "password": form_data.password})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
def login(data: Dict[str, str]):
    try:
        return auth_service.login(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/signup")
def signup(data: UserCreate):
    try:
        return auth_service.signup(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
