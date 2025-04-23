import pytest
from fastapi.testclient import TestClient
from src.config import Settings
from sqlalchemy.orm import Session
from src.main import app
from src.database import close_db_connections, get_engine, get_db

@pytest.fixture()
def app_settings() -> Settings:
    return Settings()

@pytest.fixture()
def test_password() -> str:
    return "finapi-test-password"

@pytest.fixture()
def test_get_admin_user_header(client: TestClient, test_password: str, app_settings: Settings):
    admin_test_email = 'admintestuser@finapi.com'
    data = {
        'email':admin_test_email,
        'first_name':'adminfirstname',
        'last_name': 'adminlastname',
        'password': test_password,
        'is_admin':'true',
    }
    response = client.post('/users', json=data, headers={'admin-token':app_settings.admin_signup_token})

    assert response.status_code == 200, response.json() 
    
    ##log user into the system
    user_info = {
        'username':admin_test_email,
        'password':test_password
    }
    response = client.post('/token', data=user_info)

    assert response.status_code == 200, response.json()

    data =  response.json()
    assert data['token_type'] == 'Bearer'

    return {'Authorization': f"Bearer {data['access_token']}"}

@pytest.fixture()
def test_db():
    get_engine()
    db = get_db

    try:
        yield db
    finally:
        db.close()
        close_db_connections()

@pytest.fixture()
def client():
    yield TestClient(app)