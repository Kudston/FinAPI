from datetime import datetime, timedelta
from cgi import print_form
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from src.auth.dependencies import get_current_active_user
from src.config import Settings
from src.database import get_db
from src.services import get_settings
from src.users.models import User
from src.users.schemas import UserInDb
from src.users.services import UserService


def initiate_user_service(
    current_user: UserInDb = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    app_settings: Settings = Depends(get_settings),
):
    return UserService(requesting_user=current_user, db=db, app_settings=app_settings)


def anonymous_user(
    app_settings: Settings = Depends(get_settings)
):
    return UserInDb(
        id=uuid4(),
        email="anonymous@finapi.com",
        first_name="anonymous",
        last_name="user",
        is_active=False,
        is_admin=False,
        access_begin=datetime.now(),
        access_end=datetime.now()+timedelta(minutes=app_settings.anonymous_user_access_minutes),
    )


def initiate_anonymous_user_service(
    db: Session = Depends(get_db),
    app_settings: Settings = Depends(get_settings),
    anonymous_user=Depends(anonymous_user),
):
    return UserService(requesting_user=anonymous_user, db=db, app_settings=app_settings)