from tempfile import NamedTemporaryFile
from datetime import date
from uuid import UUID
from src.services import handle_result
from fastapi import APIRouter, Depends, Query
from src.transactions.schemas import AccountOut, TransactionCreate, TransactionOut, ManyTransactionOut
from src.transactions.services import TransactionsService
from src.auth.schemas import RequestToken
from src.transactions.dependencies import initiate_transaction_service
from src.utils import OrderDirection
from typing import Optional

router = APIRouter(prefix="/transactions", tags=['Transactions'])


@router.get('/account-info', response_model=AccountOut)
def get_account_info(
    user_id: UUID,
    transactions_service: TransactionsService = Depends(initiate_transaction_service)
):
    result = transactions_service.get_account_info(user_id=user_id)
    
    return handle_result(result, AccountOut)

@router.post('/send-funds', response_model=TransactionOut)
async def send_fund(
    request: TransactionCreate,
    transactions_service: TransactionsService = Depends(initiate_transaction_service)
):
    result = transactions_service.send_fund(request=request)

    return handle_result(result, TransactionOut)

@router.post('/fund-account', response_model=AccountOut)
async def fund_account(
    user_id: UUID,
    amount: float,
    transaction_service: TransactionsService = Depends(initiate_transaction_service)
):
    result = transaction_service.fund_account(user_id=user_id, amount=amount)

    return handle_result(result, AccountOut)

@router.get('/get-transaction-history', response_model=ManyTransactionOut)
def get_transaction_history(
    user_id: UUID,
    skip: int = Query(0, description='skip'),
    limit: int =  Query(100, description='limit to retrieve'),
    order_direction: OrderDirection = Query('asc', description='desc or asc'),
    start_date: Optional[date] = Query(None, description='filter from this date'),
    end_date: Optional[date] = Query(None, description='filter until this date'),
    transaction_type: Optional[str] = Query(None, 
                                description='filter by transaction type ["credit","debits","deposit"]'),
    min_amount: Optional[float] = Query(None, description="filter by minimum amount"),
    transactions_service: TransactionsService = Depends(initiate_transaction_service)
):
    """
        Retrieves a user's transaction history, using filters specified.
    """
    result = transactions_service.get_transactions_history(
        user_id=user_id,
        skip=skip,
        limit=limit,
        order_direction=order_direction,
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type,
        min_amount=min_amount,
    )
    
    return handle_result(result=result, expected_schema=ManyTransactionOut)




