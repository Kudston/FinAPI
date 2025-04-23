from datetime import datetime, date
from uuid import UUID
from sqlalchemy.orm import Session
from src.config import Settings
from src.services import ServiceResult, success_service_result, failed_service_result
from src.users.schemas import UserInDb
from typing import Union
from src.utils import OrderDirection
from src.transactions.crud import TransactionsCrud
from src.transactions.schemas import TransactionCreate, TransactionOut, AccountOut, ManyTransactionOut
from src.users.exceptions import UserNotActiveException
from src.transactions.exceptions import (RestrictedOperationException)
from typing import Optional

class TransactionsService:
    def __init__(self, db: Session, app_settings: Settings, requesting_user: UserInDb):
        self.crud:TransactionsCrud = TransactionsCrud(db, app_settings=app_settings)
        self.requesting_user: UserInDb = requesting_user
        self.app_settings:Settings = app_settings

    def get_account_info(
        self,
        user_id: UUID
    )->Union[ServiceResult, Exception]:
        try:
            if self.requesting_user.id != user_id and not self.requesting_user.is_admin:
                raise RestrictedOperationException('Not allowed')
            
            account = self.crud.get_user_account_by_id(user_id=user_id)
            
            return success_service_result(
                AccountOut.model_validate(account)
            )
        except Exception as raised_exception:
            return failed_service_result(raised_exception)

    def send_fund(
        self,
        request: TransactionCreate
    )->Union[ServiceResult, Exception]:
        try:
            if not self.requesting_user.is_active:
                return failed_service_result(UserNotActiveException())
            
            transaction_slip = self.crud.send_fund(request=request)
            
            return success_service_result(
                TransactionOut.model_validate(transaction_slip)
            )
        except Exception as raised_exception:
            return failed_service_result(raised_exception)
        
    def fund_account(
        self,
        user_id: UUID,
        amount: float
    )->Union[ServiceResult, Exception]:
        try:
            if not self.requesting_user.is_admin:
                return failed_service_result(RestrictedOperationException())

            account = self.crud.fund_account(user_id=user_id, amount=amount)
            return success_service_result(
                AccountOut.model_validate(account.__dict__)
            )            
        except Exception as raised_exception:
            return failed_service_result(raised_exception)
        
    def get_transactions_history(
        self,
        user_id,
        skip: int,
        limit: int,
        order_direction: OrderDirection,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        transaction_type: Optional[str] = None,
        min_amount: Optional[float] = None
    )->Union[ServiceResult, Exception]:
        try:
            if self.requesting_user.id != user_id and not self.requesting_user.is_admin:
                raise Exception('operation not allowed')
            
            results = self.crud.get_transactions_history(
                user_id=user_id,
                skip=skip,
                limit=limit,
                order_direction=order_direction,
                start_date=start_date,
                end_date=end_date,
                transaction_type=transaction_type,
                min_amount=min_amount
            )

            result_dict = {
                'total':results[0],
                'transactions':results[1]
            }

            return success_service_result(
                ManyTransactionOut.model_validate(result_dict)
            )
        except Exception as raised_exception:
            return failed_service_result(raised_exception)
