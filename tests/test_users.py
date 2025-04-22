from datetime import datetime, timedelta
from email import header
import pytest
from fastapi.testclient import TestClient

from src.config import Settings


email_under_test = "user1@finapi.com"
prefix = "http-user"


def test_root_endpoint(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200, response.json()
    assert "message" in response.json()
    assert response.json()["detail"] == "Welcome to finapi"

def test_create_user(client: TestClient, test_password: str) -> None:
    user_data = {
        'email':email_under_test,
        'first_name':'finapifirstname',
        'last_name': 'finapilastname',
        'password': test_password
    }
    response = client.post(
        '/users/',
        json=user_data
    )

    assert response.status_code == 200
    data = response.json()

    assert data['email'] == email_under_test

def test_cannot_create_duplicate_user(client: TestClient, test_password: str)->None:
    user_data = {
        'email':email_under_test,
        'first_name':'finapifirstname',
        'last_name': 'finapilastname',
        'password': test_password
    }
    response = client.post(
        '/users/',
        json=user_data
    )

    assert response.status_code != 200

def 