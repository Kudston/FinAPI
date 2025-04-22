from src.schemas import BasePydanticModel
from uuid import UUID
from typing import List

class AccessToken(BasePydanticModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BasePydanticModel):
    id: UUID
    email: str
    is_admin: bool

class RequestToken(BasePydanticModel):
    token: str