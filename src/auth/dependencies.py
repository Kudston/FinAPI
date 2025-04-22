"""Dependencies"""


from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from jose import jwt, JWTError

from pydantic import ValidationError

from fastapi import Header, HTTPException, status, Depends, Security
from fastapi.security import SecurityScopes
from src.auth.schemas import TokenData
from src.config import Settings
from src.database import get_db

from src.security import get_user, oauth2_scheme
from src.services import get_settings
from src.users.schemas import UserInDb


def has_admin_token_in_header(
    app_settings: Settings, 
    admin_access_token: str = Header(None, alias='ADMIN_SIGNUP_TOKEN')
):
    """Verifies if the header has an admin token"""

    if admin_access_token != app_settings.admin_signup_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin-Access-Token header invalid",
        )

def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    app_settings: Settings = Depends(get_settings),
):

    authenticate_value = "Bearer"
        
    credentials_exception = Exception('invalid authentication credentials')
    
    try:
        payload = jwt.decode(
            token=token,
            key=app_settings.secret_key,
            algorithms=[app_settings.algorithm],
        )

        email: str = payload.get("sub", None)  
        user_id: str = payload.get("id", None)  
        is_admin: bool = payload.get("is_admin", None)
        
        if email is None or user_id is None or is_admin is None:
            raise credentials_exception
        
        token_data = TokenData(
            id=UUID(user_id),
            is_admin=is_admin,
            email=email
        )

    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(db, username=token_data.email)

    if user is None:
        raise credentials_exception
        
    return user


def get_current_active_user(
    current_user: UserInDb = Security(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return current_user


def user_must_be_admin(current_user: UserInDb = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return current_user


def is_admin_signup_token(
    token: str,
    app_settings: Settings
):
    if token!=app_settings.admin_signup_token:
        raise Exception("ADMIN TOKEN PROVIDED IS NOT CORRECT.")
