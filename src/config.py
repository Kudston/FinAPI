import os

class Settings:
    def __init__(self):
        pass

    ##jwt settings
    secret_key = os.getenv('SECRET_KEY','supersecretkey')
    algorithm = os.getenv('ALGORITHM', 'HS256')
    access_code_expiring_minutes = int(os.getenv('ACCESS_CODE_EXPIRING_MINUTES', 30))
    request_password_token_expiring_minutes = int(os.getenv('REQUEST_PASSWORD_TOKEN_EXPIRING_MINUTES', 30))
    verify_email_token_expiring_minutes = int(os.getenv('VERIFY_EMAIL_TOKEN_EXPIRING_MINUTES', 30))
    anonymous_user_access_minutes = int(os.getenv('ANONYMOUS_USER_ACCESS_MINUTES','3600'))

    ##database settings 
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_host = os.getenv('DB_HOST')
    db_port = int(os.getenv('DB_PORT'))
    db_password = os.getenv('DB_PASSWORD')

    ##admin related settings
    admin_signup_token = os.getenv('ADMIN_SIGNUP_TOKEN', 'superadminsignupfaketoken')
    app_name = os.getenv('APP_NAME','finAPI')
    admin_email = os.getenv('SUPER_ADMIN_EMAIL','admin@gmail.com')
    admin_password = os.getenv('SUPER_ADMIN_PASSWORD','adminpassword')
    

    ##account creation parameters
    max_tries_creating_account_number = int(os.getenv('MAX_TRIES_CREATING_ACCOUNT_NUMBER', '10'))
    minimum_transaction_amount  = float(os.getenv('MINIMUM_TRANSACTION_AMOUNT', '0'))

    def get_full_db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

