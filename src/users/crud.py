from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from src.config import Settings
from src.users.models import User, Profile
from typing import Union, List
from src.users import schemas
from src.security import get_password_hash
from src.users.exceptions import UserNotFoundException
from src.security import (
    generate_request_password_token,
    generate_verify_email_token, 
    decode_token
    )
from src.transactions.crud import TransactionsCrud

class UserCRUD:
    def __init__(
        self, 
        db: Session, 
        app_settings: Settings
    ):
        self.db = db
        self.settings = app_settings
        self.transaction_crud = TransactionsCrud(db, app_settings=app_settings)

    def get_user_by_email(self, email: str) -> User:
        try:
            user = self.db.query(User).filter(User.email == email).first()
            return user
        except Exception as raised_exception:
            raise raised_exception

    def get_user_by_id(self, user_id: int) -> User:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            return user
        except Exception as raised_exception:
            raise raised_exception

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        try:
            users = self.db.query(User).offset(skip).limit(limit).all()
            return users
        except Exception as raised_exception:
            raise raised_exception
        
    def check_user_exists(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email).first() is not None

    def create_user(self, user_info: schemas.UserCreate) -> User:
        try:
            db_user = User(
                email=user_info.email,
                first_name=user_info.first_name,
                last_name=user_info.last_name,
                hashed_password=get_password_hash(user_info.password),
                is_active=False,
                is_admin=user_info.is_admin,
                access_begin=datetime.now(),
                access_ends=datetime.now()
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)

            db_profile = self.create_profile(db_user.id)

            db_account = self.transaction_crud.create_account(db_user.id)
            
            self.db.refresh(db_user)
            return db_user
        except Exception as raised_exception:
            self.db.rollback()
            print(raised_exception)
            raise raised_exception

    def update_user(self, user_id: UUID, data: schemas.UserUpdate):
        user: User = self.get_user_by_id(user_id)
        if not user:
            return UserNotFoundException()

        data_without_none: dict = data.model_dump(exclude_none=True)

        for key in data_without_none:
            setattr(user, key, data_without_none[key])

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user


    def create_profile(self, user_id: UUID):
        try:
            db_profile = Profile(user_id=user_id)
            
            self.db.add(db_profile)
            self.db.commit()
            self.db.refresh(db_profile)
            return db_profile
        except  Exception as raised_exception:
            raise raised_exception

    def update_user_profile(
        self,
        user_id,
        profile_update: schemas.ProfileUpdate
    ):
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise Exception("No user found for id.")
            
            profile = self.db.query(Profile).filter(Profile.user_id==user_id).first()
            
            if not profile:
                raise Exception("No profile found for id.")
            
            data_without_none: dict = profile_update.model_dump(exclude_unset=True)

            for key, value in data_without_none.items():
                setattr(profile, key, value)

            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
            return profile
        except Exception as raised_exception:
            raise raised_exception
        
    def update_user_profile_photo(
        self, user_id: UUID, file_object_id: UUID
    ):
        db_profile = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )
        if db_profile is None:
            raise Exception("The profile does not exist.")

        setattr(db_profile, "photo_file_id", file_object_id)

        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)

        return db_profile

    def delete_user(self, user_id: int) -> bool:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found")

            profile = self.db.query(Profile).filter(Profile.user_id == user_id).delete(
                synchronize_session=False
            )

            users = self.db.query(User).filter(User.id == user_id).delete(synchronize_session=False)
            
            return True
        except Exception as raised_exception:
            self.db.rollback()
            raise raised_exception

    def generate_password_reset_token(
        self,
        user_id
    ):
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundException(f"User with ID {user_id} does not exist")
            
            token = generate_request_password_token(
                user=user,
                app_settings=self.settings,
            )
            return token
        except Exception as raised_exception:
            raise raised_exception
        
    def update_user_password(self, reset_token, new_password: str) -> User:
        try:
            payload = decode_token(token=reset_token, app_settings=self.settings)
            if payload.exp.timestamp() < datetime.now().timestamp():
                raise ValueError("Token expired")
            
            user = self.get_user_by_id(payload["id"])
            if not user:
                raise UserNotFoundException(f"User with ID {payload['id']} does not exist")

            setattr(user, "hashed_password", get_password_hash(new_password))

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user
        except Exception as raised_exception:
            raise raised_exception