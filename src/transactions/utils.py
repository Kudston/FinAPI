import enum

class TransactionStatus(enum.Enum):
    Success = "Success"
    Failed  = "Failed"
    Pending = "Pending"

class TransactionTypes(enum.Enum):
    credit = "credit"
    debit  = "debit"
    deposit = "deposit"