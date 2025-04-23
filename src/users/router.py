from io import BytesIO
from tempfile import NamedTemporaryFile

from uuid import UUID
from pydantic import EmailStr
from src.services import handle_result
from fastapi import APIRouter, Depends, Header, Query
from fastapi.responses import FileResponse
from src.users.schemas import UserCreate, UserInDb, UserUpdate, ManyUsersInDb
from src.users.services import UserService
from src.users.dependencies import initiate_user_service, initiate_anonymous_user_service
from src.auth.schemas import RequestToken

router = APIRouter(prefix="/users", tags=['Users'])

@router.get('/', response_model=ManyUsersInDb)
def get_users(
    skip: int = 0,
    limit: int = 100,
    user_services: UserService = Depends(initiate_user_service)
):
    result = user_services.get_users(skip=skip, limit=limit)
    return handle_result(result, expected_schema=ManyUsersInDb)

@router.post('/', response_model=UserInDb)
async def create_user(
    user_info: UserCreate,
    admin_token: str = Header(None, max_length=50, description="super admin token for admin operations"),
    user_service: UserService = Depends(initiate_anonymous_user_service)
):
    result = await user_service.create_user(user_info=user_info, admin_token=admin_token)
    
    return handle_result(result, expected_schema=UserInDb)

@router.get('/get-user-by-id', response_model=UserInDb)
def get_user_by_id(
    id: UUID,
    user_service: UserService = Depends(initiate_user_service)
):
    """
    Get user by id.
    """
    result = user_service.get_user_by_id(id=id)
    return handle_result(result, expected_schema=UserInDb)

@router.put('/update-user/{id}')
def update_user(
    id: UUID,
    user_info: UserUpdate,
    user_service: UserService = Depends(initiate_user_service)
):
    """
    Update user information.
    """
    result = user_service.update_user(id=id, user=user_info)
    return handle_result(result, expected_schema=UserInDb)

@router.get('/request-password-reset', response_model=RequestToken)
async def request_reset_password(
    email: EmailStr,
    user_service: UserService = Depends(initiate_anonymous_user_service)
):
    result = await user_service.generate_password_reset_token(email=email)

    return handle_result(result, expected_schema=RequestToken)

@router.post('/reset-password', response_model=UserInDb)
def reset_password(
    token: str = Query(..., max_length=255),
    new_password: str = Query(..., max_length=255),
    user_service: UserService = Depends(initiate_anonymous_user_service)
):
    result = user_service.update_user_password(token=token, new_password=new_password)
    return handle_result(result, expected_schema=UserInDb)