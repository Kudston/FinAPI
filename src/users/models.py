from src.models import Base
from uuid import uuid4
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), index=True, unique=True, primary_key=True, default=uuid4)

    email = Column(String(), unique=True)
    hashed_password = Column(String())
    first_name = Column(String())
    last_name  = Column(String())

    created_on = Column(DateTime(), default=func.now())
    modified_on = Column(DateTime(), onupdate=func.now(), nullable=True)

    is_active  = Column(Boolean(), default=False)
    is_verified = Column(Boolean(), default=False)
    is_admin    = Column(Boolean(), default=False)

    access_begin = Column(DateTime(), nullable=False)
    access_ends  = Column(DateTime(), nullable=False)

    profile = relationship('Profile', back_populates='user', lazy='joined')
    account = relationship('Account', back_populates='user', lazy='joined')

    @property
    def get_fullname(self)->str:
        return f'{self.first_name}+{self.last_name}'

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), index=True, unique=True, primary_key=True, default=uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    user    = relationship(User, foreign_keys=[user_id], lazy='joined')

    created_on = Column(DateTime(), default=func.now())
    modified_on = Column(DateTime(), onupdate=func.now(), nullable=True)


