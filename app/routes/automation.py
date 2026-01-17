from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_tenant

router = APIRouter(prefix="/automation", tags=["automation"])

@router.get("/status")
def status():
    return {"status": "AI Active"}
