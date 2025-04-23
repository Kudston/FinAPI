from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends
from src.auth.dependencies import get_current_active_user
from src.config import Settings
from src.database import get_db
from src.services import get_settings
from src.users.schemas import UserInDb
from src.transactions.services import TransactionsService

def initiate_transaction_service(
    current_user: UserInDb = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    app_settings: Settings = Depends(get_settings),
):
    return TransactionsService(requesting_user=current_user, db=db, app_settings=app_settings)



