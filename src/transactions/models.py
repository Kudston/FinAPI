from src.models import Base
from uuid import uuid4
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Boolean,
    ForeignKey,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from src.users.models import User

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), index=True, unique=True, primary_key=True, default=uuid4)

    account_number = Column(String(length=10), unique=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user    = relationship(User, foreign_keys=[user_id], back_populates='account', lazy='joined')

    date_created = Column(DateTime(), default=func.now())
    date_modified = Column(DateTime(), onupdate=func.now(), nullable=True)

    account_balance = Column(Float(precision=2))
    transfer_pin    = Column(String(), nullable=True)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), index=True, unique=True, primary_key=True, default=uuid4)

    credited_account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'))
    credited_account = relationship(Account, foreign_keys=[credited_account_id], lazy='joined')

    debited_account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'))
    debited_account    = relationship(Account, foreign_keys=[debited_account_id], lazy='joined')

    transaction_status = Column(String(), default=False)
    amount             = Column(Float(precision=2), nullable=False)

    date_created = Column(DateTime(), default=func.now())

