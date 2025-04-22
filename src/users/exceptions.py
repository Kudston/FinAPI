from fastapi import HTTPException, status

class UserNotFoundException(Exception):
    pass

class UserNotActiveException(Exception):
    pass
