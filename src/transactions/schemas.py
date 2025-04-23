from uuid import UUID
from src.schemas import BasePydanticModel
from pydantic import constr
from typing import Optional, List

class TransactionCreate(BasePydanticModel):
    debited_account_number: str
    credited_account_number: str
    amount: float
    note: Optional[str] = None #type:ignore

class TransactionOut(BasePydanticModel):
    id: UUID
    sender_name: str
    recipients_name: str
    recipients_account_number: str
    note: Optional[str] = None

class AccountOut(BasePydanticModel):
    id: UUID
    account_number: str
    account_balance: float

class ManyTransactionOut(BasePydanticModel):
    total: int
    transactions: List[TransactionOut]

