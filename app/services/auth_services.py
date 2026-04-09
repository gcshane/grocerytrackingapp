from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pwdlib import PasswordHash
from jwt import encode, decode, InvalidTokenError, ExpiredSignatureError

from app.services.user_services import get_user_by_username, get_user_by_id
from app.dependencies import SessionDep
from app.core.config import config
from app.models.auth import Token

password_hash = PasswordHash.recommended()
access_token_expires = timedelta(minutes = int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
secret_key = config.JWT_SECRET_KEY
algorithm = config.JWT_ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def login_service(session: SessionDep, form_data: OAuth2PasswordRequestForm):
    user = get_user_by_username(form_data.username, session)
    if not user or not password_hash.verify(form_data.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    data = {"sub" : str(user.user_id), "exp" : int((datetime.now(timezone.utc) + access_token_expires).timestamp())}
    encoded_jwt = encode(data, secret_key, algorithm)
    token = Token(access_token = encoded_jwt, token_type = "bearer")
    return token

async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode(token, secret_key, algorithms = [algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Token expired",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_id(user_id, session)
    if user is None:
        raise credentials_exception
    return user
