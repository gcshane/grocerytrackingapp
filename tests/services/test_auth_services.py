import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from unittest.mock import patch, MagicMock
from jwt import encode
from datetime import datetime, timezone, timedelta

from app.db.schema import User
from app.services.auth_services import login_service, password_hash, get_current_user, decode_jwt_token, secret_key, algorithm
def test_login_service_successful():
    real_password = "my_secret_password"
    fake_user = User(
        user_id=1,
        username="test_user", 
        name="Test", 
        email="test@test.com", 
        password=password_hash.hash(real_password), 
        alert=True
    )
    
    with patch("app.services.auth_services.get_user_by_username") as mock_get_user:
        mock_get_user.return_value = fake_user
        
        fake_form_data = OAuth2PasswordRequestForm(username="test_user", password=real_password)
        
        dummy_session = MagicMock()
        
        token = login_service(dummy_session, fake_form_data)
        
        assert token is not None
        assert token.token_type == "bearer"
        assert token.access_token is not None

def test_login_service_wrong_password():
    fake_user = User(
        user_id=1,
        username="test_user", 
        name="Test", 
        email="test@t.com", 
        password=password_hash.hash("correct_password"), 
        alert=True
    )

    with patch("app.services.auth_services.get_user_by_username") as mock_get_user:
        mock_get_user.return_value = fake_user
        
        fake_form_data = OAuth2PasswordRequestForm(username="test_user", password="WRONG_PASSWORD")
        dummy_session = MagicMock()

        with pytest.raises(HTTPException) as exception_info:
            login_service(dummy_session, fake_form_data)
        
        assert exception_info.value.status_code == 401
        assert exception_info.value.detail == "Invalid credentials"

@pytest.mark.anyio
async def test_get_current_user_successful():
    fake_user = User(
        user_id=1,
        username="test_user", 
        name="Test", 
        email="test@t.com", 
        password=password_hash.hash("correct_password"), 
        alert=True
    )

    with patch("app.services.auth_services.get_user_by_id") as mock_get_user:
        mock_get_user.return_value = fake_user
        dummy_session = MagicMock()

        # Notice how we don't need a token anymore! We just prove it can fetch the user!
        user = await get_current_user(dummy_session, user_id="1")

        assert user.user_id == 1
        assert user.username == "test_user"

@pytest.mark.anyio
async def test_get_current_user_not_found():
    with patch("app.services.auth_services.get_user_by_id") as mock_get_user:
        mock_get_user.return_value = None
        dummy_session = MagicMock()

        with pytest.raises(HTTPException) as exception_info:
            await get_current_user(dummy_session, user_id="999")
            
        assert exception_info.value.status_code == 401
        assert exception_info.value.detail == "Could not validate credentials"

def test_decode_jwt_token_successful():
    data = {"sub": "1"}
    fake_valid_token = encode(data, secret_key, algorithm)

    user_id = decode_jwt_token(token=fake_valid_token)
    assert user_id == "1"

def test_decode_jwt_token_invalid_token():
    bad_token = "this.is.obviously.not.a.real.jwt"

    with pytest.raises(HTTPException) as exception_info:
        decode_jwt_token(token=bad_token)
    
    assert exception_info.value.status_code == 401
    assert exception_info.value.detail == "Could not validate credentials"

def test_decode_jwt_token_expired_token():
    data = {
        "sub": "1",
        "exp": int((datetime.now(timezone.utc) - timedelta(minutes=10)).timestamp())
    }
    expired_token = encode(data, secret_key, algorithm)

    with pytest.raises(HTTPException) as exception_info:
        decode_jwt_token(token=expired_token)
    
    assert exception_info.value.status_code == 401
    assert exception_info.value.detail == "Token expired"