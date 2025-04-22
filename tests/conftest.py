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