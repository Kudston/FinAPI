from uuid import UUID
from src.schemas import BasePydanticModel
from pydantic import constr
from typing import Optional, List

class TransactionCreate(BasePydanticModel):
    debited_user_id: UUID
    credited_user_id: UUID
    amount: float
    note: Optional[constr(max_length=100)] #type:ignore

class TransactionOut(BasePydanticModel):
    id: UUID

    sender_name: str
    recepients_name: str

    recepient_account_no: str

    note: str

class AccountOut(BasePydanticModel):
    id: UUID
    account_number: str
    account_balance: float

class ManyTransactionOut(BasePydanticModel):
    total: int 
    transactions: List[TransactionOut]    

