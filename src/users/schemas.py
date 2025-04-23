from uuid import UUID
from src.schemas import BasePydanticModel
from pydantic import EmailStr, constr
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class UserCreate(BasePydanticModel):
    email: EmailStr
    first_name: constr(max_length=64) #type:ignore
    last_name: constr(max_length=64)  #type:ignore
    password: str

    is_admin: Optional[bool] = False

class UserInDb(BasePydanticModel):
    id: UUID
    email: EmailStr
    first_name: Optional[constr(max_length=64)] #type:ignore
    last_name: Optional[constr(max_length=64)]  #type:ignore

    nin_verified: Optional[bool] = False
    facials_verified: Optional[bool] = False

    access_begin: Optional[datetime] = None
    access_ends: Optional[datetime] = None

    is_active: bool
    is_admin: bool

class ManyUsersInDb(BasePydanticModel):
    total: int
    users: List[UserInDb]

class UserUpdate(BasePydanticModel):
    first_name: Optional[constr(max_length=64)] = None #type:ignore
    last_name: Optional[constr(max_length=64)] = None #type:ignore

    access_begin: Optional[datetime]
    access_end: Optional[datetime] 
    is_active: Optional[bool] = False


class ProfileUpdate(BasePydanticModel):
    pass

class ProfileOut(BasePydanticModel):
    id: UUID
    user_id: UUID
    user: UserInDb

