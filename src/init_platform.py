from datetime import datetime, timedelta
from src.database import get_db
from src.users.crud import UserCRUD
from src.config import Settings
from src.users.schemas import UserCreate


def create_admin_user():
    db = next(get_db())  # Get the actual session
    try:
        app_settings = Settings()
        user_crud = UserCRUD(db, app_settings)
        existing_admin_user = user_crud.get_user_by_email(app_settings.admin_email)
        if existing_admin_user:
            print('Admin user already exists.')
            return

        user = user_crud.create_user(
            UserCreate(
                email=app_settings.admin_email,
                first_name="adminfirstname",
                last_name="adminlastname",
                password=app_settings.admin_password,
                is_admin=True,
                access_begin=datetime.now(),
                access_end=datetime.now() + timedelta(days=365)
            )
        )

        print('Admin user created successfully.')
    finally:
        db.close()