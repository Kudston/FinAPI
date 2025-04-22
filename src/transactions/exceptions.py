from fastapi import HTTPException, status

class InsufficientBalanceException():
    pass

class UserAccountDoesNotExistException(Exception):
    pass

class TransferAmountTooSmallException(Exception):
    pass

class RestrictedOperationException(Exception):
    pass