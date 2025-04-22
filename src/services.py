from pydantic import BaseModel
from src.schemas import AppResponseModel
from fastapi import HTTPException, status
from src.config import Settings

class ServiceResult():
    def __init__(self, success: str, data: dict, message: str, exception: Exception=None):
        self.success = success
        self.data = data
        self.message = message
        self.exception = exception

def success_service_result(data:dict):
    return ServiceResult(True, data, "")

def failed_service_result(exception: Exception):
    return ServiceResult(False, {}, "", exception)

def handle_result(result: ServiceResult, expected_schema: BaseModel = None):  # type: ignore
    """Handles the result returned from any service in the application, both failures and successes."""

    try:
        if expected_schema is not None:
            return expected_schema.model_validate(result.data)
        else:
            return AppResponseModel(detail=result.data)
    except Exception as raised_exception:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail=str(raised_exception))
                
def get_settings():
    return Settings()