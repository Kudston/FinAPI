from datetime import datetime, timedelta
from typing import Any
from uuid import UUID
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from jose import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import status
from src.auth.exceptions import invalid_authentication_credentials_exception
from src.users import models
from src.users.exceptions import UserNotFoundException

from src.users.schemas import UserInDb
from src.config import Settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token", scopes={"me": "Read information about the current user."}
)


def fake_hash_password(password: str):
    return "fakehashed" + password



def decode_token(token: str, secret_key: str, algorithm: str):
    payload = jwt.decode(
        token=token,
        key=secret_key,
        algorithms=[algorithm],
    )

    return payload


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> models.User:
    user: models.User = db.query(models.User).filter(models.User.email == username).first()  # type: ignore
    if not user:
        raise UserNotFoundException(f"User with email {username} not found")

    return user


def authenticate_user(db: Session, username: str, password: str):
    user: UserInDb = get_user(db, username)

    if not verify_password(password, str(user.hashed_password)):
        raise invalid_authentication_credentials_exception()

    return user


def create_access_token(
    data: dict[str, Any],
    secret_key: str,
    algorithm: str,
    expires_delta: timedelta = None, 
):
    to_encode: dict[str, Any] = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return encoded_jwt

def generate_request_password_token(
        user: models.User,
        app_settings: Settings
):
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You don't have a verified account. contact admin.",
        )
    token_expires = datetime.now()+timedelta(minutes=app_settings.request_password_token_expiring_minutes)
    token_data = {
        "id": str(user.id),
        "sub": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "exp": token_expires
    }
    token = create_access_token(
        data=token_data,
        secret_key=app_settings.secret_key,
        algorithm=app_settings.algorithm,
        expires_delta=timedelta(minutes=app_settings.request_password_token_expiring_minutes)
    )

def generate_verify_email_token(
        user: models.User,
        app_settings: Settings
):
    token_expires = datetime.now()+timedelta(minutes=app_settings.verify_email_token_expiring_minutes)
    token_data = {
        "id": str(user.id),
        "sub": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "exp": token_expires
    }
    token = create_access_token(
        data=token_data,
        secret_key=app_settings.secret_key,
        algorithm=app_settings.algorithm,
        expires_delta=timedelta(minutes=app_settings.verify_email_token_expiring_minutes)
    )
    return token

