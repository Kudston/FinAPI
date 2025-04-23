from pydantic import BaseModel
from src.schemas import AppResponseModel
from fastapi import HTTPException, status
from src.config import Settings
from src.exceptions import handle_bad_request_exception

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

    if result.success:
        try:
            if expected_schema is not None:
                return expected_schema.from_orm(result.data)
            else:
                return AppResponseModel(detail=result.data)
        except Exception as raised_exception:
            handle_bad_request_exception(raised_exception)
    else:
        handle_bad_request_exception(result.exception)
                
def get_settings():
    return Settings()