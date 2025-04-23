from pydantic import BaseModel, ConfigDict

class BasePydanticModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class AppResponseModel(BasePydanticModel):
    detail: str