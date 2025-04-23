from fastapi import HTTPException, status

def handle_bad_request_exception(exception: Exception):
    """Raises an 400 HTTPException"""

    raise HTTPException(
        detail=str(exception), status_code=status.HTTP_400_BAD_REQUEST
    ) from exception
