from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.auth.schemas import AccessToken

from src.config import Settings
from src.database import get_db
from src.services import get_settings   
from src.security import authenticate_user, create_access_token
from src.users.exceptions import UserNotFoundException
from src.users.schemas import UserUpdate
from src.users.services import UserService

router = APIRouter(tags=["Auth"])

router = APIRouter()


@router.post("/token", response_model=AccessToken)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    app_settings: Settings = Depends(get_settings),
):
    """
    Authenticates with the given credentials.

    **Note**, passwords are case sensitive.
    """

    try:
        user = authenticate_user(db, form_data.username, form_data.password)

        user_service: UserService = UserService(
            requesting_user=user, db=db, app_settings=app_settings
        )

        user_service.update_user(
            user_id=user.id,
            update_info=UserUpdate(
                is_active=True,
                access_begin=datetime.now(), 
                access_end=datetime.now()+timedelta(minutes=app_settings.access_code_expiring_minutes)),
        )

    except UserNotFoundException as raised_exception:
        raise raised_exception
    
    access_token_expires = timedelta(minutes=app_settings.access_code_expiring_minutes)
   
    access_token_data = {
        "id": str(user.id),
        "sub": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }

    access_token = create_access_token(
        data=access_token_data,
        secret_key=app_settings.secret_key,
        algorithm=app_settings.algorithm,
        expires_delta=access_token_expires,
    )

    token = AccessToken(access_token=access_token)
    return token