import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from src.config import Settings
from src.services import ServiceResult, success_service_result, failed_service_result
from src.users.schemas import UserCreate, UserUpdate, UserInDb, ProfileOut, ProfileUpdate,ManyUsersInDb
from typing import Union
from src.utils import OrderBy, OrderDirection
from src.users.crud import UserCRUD
from src.users.exceptions import UserNotFoundException
from src.schemas import AppResponseModel
from src.auth.dependencies import is_admin_signup_token

class UserService:
    def __init__(self, db: Session, app_settings: Settings, requesting_user: UserInDb):
        self.crud:UserCRUD = UserCRUD(db, app_settings=app_settings)
        self.requesting_user: UserInDb = requesting_user
        self.app_settings:Settings = app_settings

    async def create_user(
        self,
        admin_token: str,
        user_info: UserCreate
    )->Union[ServiceResult, Exception]:
        try:
            if user_info.is_admin:
                is_admin_signup_token(token=admin_token, app_settings=self.app_settings)

            user = self.crud.create_user(user_info=user_info)
            
            return success_service_result(
                UserInDb.model_validate(user.__dict__)
            )
        except Exception as raised_exception:
            print(raised_exception)
            return failed_service_result(exception=raised_exception)
        
    def get_user_by_id(
        self,
        user_id:UUID
    )->Union[ServiceResult, Exception]:
        try:
            pass
        except Exception as raised_exception:
            return failed_service_result(raised_exception)
    
    def get_users(
        self,
        skip: int,
        limit: int,
    )->Union[ServiceResult, Exception]:
        try:
            users = self.crud.get_users(skip=skip, limit=limit)
            result = {
                'total': len(users),
                'users': users
            }
            return success_service_result(
                ManyUsersInDb.model_validate(result)
            )
        except Exception as raised_exception:
            return failed_service_result(raised_exception)

    def update_user(
        self,
        user_id: UUID,
        update_info: UserUpdate
    )->Union[ServiceResult, Exception]:
        try:
            print('came here already')
            if self.requesting_user.id != user_id and not self.requesting_user.is_admin:
                return failed_service_result("You are not allowed to perform action.")
            
            user = self.crud.update_user(user_id=user_id, data=update_info)

            return success_service_result(
                data=UserInDb.model_validate(user.__dict__)
            )
        except Exception as raised_exception:
            return failed_service_result(raised_exception)
        
    def update_user_profile(
        self,
        profile_update: ProfileUpdate
    )->Union[ServiceResult, Exception]:
        try:
            profile = self.crud.update_user_profile(
                self.requesting_user.id,
                profile_update
            )
            return success_service_result(
                data=ProfileOut.model_validate(profile.__dict__)
            )
        except Exception as raised_exception:
            return failed_service_result(raised_exception)

    async def generate_password_reset_token(
        self,
        user_email: str
    )->Union[ServiceResult, Exception]:
        try:
            ##check if the user exists
            user = self.crud.get_user_by_email(user_email)
            if not user:
                raise UserNotFoundException("User does not exist.")
            
            token = self.crud.generate_password_reset_token(user_id=self.requesting_user.id)
            ##send the token to user using email service
            email_body = {
                "full_name": self.requesting_user.first_name+" "+self.requesting_user.last_name,
                "reset_link": token,
                "current_year": datetime.datetime.now().year,
                "company_name": self.app_settings.app_name,
            }
            # email = EmailSchema(
            #     emails=[user_email],
            #     body=email_body
            # )
            # await send_verify_user_email(email)
            return success_service_result(AppResponseModel(
                message="successfully sent the reset token to user email"
            ))
        except Exception as raised_exception:
            return failed_service_result(raised_exception)
        
    def update_user_password(
        self,
        reset_token: str,
        new_password: str
    )->Union[ServiceResult, Exception]:
        try:
            user = self.crud.update_user_password(reset_token=reset_token, new_password=new_password)
            return success_service_result(UserInDb.model_validate(user.__dict__))
        except Exception as raised_exception:
            return failed_service_result(raised_exception)