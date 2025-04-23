import random
from uuid import UUID
from datetime import datetime, date
from sqlalchemy.orm import Session
from src.config import Settings
from typing import Union, List
from src.transactions.models import Transaction, Account
from src.transactions.schemas import TransactionCreate, TransactionOut
from src.transactions.exceptions import (
    InsufficientBalanceException,
    UserAccountDoesNotExistException,
    TransferAmountTooSmallException
    )
from src.transactions.utils import TransactionStatus, TransactionTypes
from sqlalchemy import or_
from src.utils import OrderBy, OrderDirection
from typing import Optional

class TransactionsCrud:
    def __init__(self, db: Session, app_settings: Settings):
        self.db = db
        self.app_settings = app_settings

    def send_fund(
        self,
        request: TransactionCreate
    )-> TransactionOut:
        try:
            debited_account = self.db.query(Account).filter(Account.user_id == request.debited_user_id).first()
            if debited_account.account_balance < request.amount:
                raise InsufficientBalanceException()
            
            if request.amount < self.app_settings.minimum_transaction_amount:
                raise Exception(f"Minimum allowed for transfer is {self.app_settings.minimum_transaction_amount}")

            credited_account  = self.db.query(Account).filter(Account.user_id == request.credited_user_id).first()
            
            ##edit their account balance
            #debited
            setattr(debited_account, 'account_balance', debited_account.account_balance - request.amount)

            #credited
            setattr(credited_account, 'account_balance',credited_account.account_balance + request.amount)

            new_transaction = Transaction(
                credited_account_id = credited_account.id,
                debited_account_id = debited_account.id,
                amount  = request.amount,
                transaction_status = TransactionStatus.Success.value
            )

            self.db.add_all([new_transaction, credited_account, debited_account])
            self.db.commit()
            self.db.refresh(new_transaction)

            transaction_out = TransactionOut(
                id= new_transaction.id,
                sender_name= debited_account.user.get_fullname,
                recipients_name= credited_account.user.get_fullname,
                recipients_account_number= credited_account.account_number,
            )
            return transaction_out
        except Exception as raised_exception:
            self.db.rollback()
            return raised_exception

    def generate_account_number(self):
        base_number = random.randint(100000, 999999)
    
        check_digits = random.randint(1000, 9999)
        
        account_number = f"{base_number}{check_digits}"
        
        return account_number
    
    def is_account_no_already_used(self, number: str):
        return self.db.query(Account).filter(Account.account_number == number).first() is not None
    
    def create_account(
        self,
        user_id: UUID
    )->Account:
        try:
            account_no = self.generate_account_number()
            tries = 0
            while self.is_account_no_already_used(account_no) and tries < self.app_settings:
                account_no = self.generate_account_number()
                tries += 1

            account = Account(
                account_number = account_no,
                user_id = user_id,
                account_balance = 0.0
            )

            self.db.add(account)
            self.db.commit()
            self.db.refresh(account)
            return account
        except Exception as raised_exception:
            raise raised_exception
        
    def fund_account(
        self,
        user_id: str,
        amount: float,
    )->Account:
        try:
            user_account = self.db.query(Account).filter(Account.user_id == user_id).first()
            
            if not  user_account:
                raise UserAccountDoesNotExistException(user_id=user_id)
            
            if amount < self.app_settings.minimum_transaction_amount:
                raise TransferAmountTooSmallException(self.app_settings.minimum_transaction_amount)
            
            setattr(user_account, 'account_balance', user_account.account_balance + amount)

            self.db.add(user_account)
            self.db.commit()
            self.db.refresh(user_account)

            return user_account
        except Exception as raised_exception:
            raise raised_exception
        
    def get_user_account_by_id(
        self,
        user_id: UUID
    )-> Account:
        try:
            user_account = self.db.query(Account).filter(Account.user_id == user_id).first()
            if not user_account:
                raise UserAccountDoesNotExistException()
            
            return user_account
        except Exception as raised_exception:
            raise raised_exception
        
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
    ):
        """
            Returns (counts, transactions)
        """

        try:
            account = self.db.query(Account).filter(Account.user_id == user_id).first()
            
            if not account:
                raise UserAccountDoesNotExistException()

            query = self.db.query(Transaction)

            #check requested transaction type
            if transaction_type is not None:
                if transaction_type == TransactionTypes.credit.value:
                    query = query.filter(Transaction.credited_account_id == account.id)
                elif transaction_type == TransactionTypes.debit.value:
                    query = query.filter(Transaction.debited_account_id == account.id)
            else:
                query = query.filter(or_(
                    Transaction.credited_account_id == account.id,
                    Transaction.debited_account_id == account.id
                ))
            
            if min_amount is not None:
                query = query.filter(Transaction.amount >= min_amount)
            
            if start_date is not None:
                query = query.filter(Transaction.date_created >= start_date)
            if end_date is not None:
                query = query.filter(Transaction.date_created<=end_date)

            order_object = Transaction.date_created.desc()
            if order_direction == OrderDirection.ASC.value:
                order_object = Transaction.date_created.asc()
            
            query = query.order_by(order_object)
            counts = query.count()

            transactions = query.offset(skip).limit(limit).all()
            transactions_out = [TransactionOut(
                id= transaction.id,
                sender_name= transaction.debited_account.user.get_fullname,
                recipients_name= transaction.credited_account.user.get_fullname,
                recipients_account_number= transaction.credited_account.account_number,
            ) for transaction in transactions]
            return (counts, transactions_out)
        except Exception as raised_exception:
            raise raised_exception
        
    