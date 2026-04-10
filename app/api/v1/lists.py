from fastapi import APIRouter, Depends
from app.services.auth_services import get_current_user

router = APIRouter()

@router.get("/lists")
async def get_lists(current_user = Depends(get_current_user)):
    return {"message": "Return all lists for user."}