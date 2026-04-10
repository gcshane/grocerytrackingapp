from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import SessionDep
from app.services.auth_services import login_service

router = APIRouter()

@router.post("/auth/login")
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    return login_service(session, form_data)