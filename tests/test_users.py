from fastapi.testclient import TestClient

email_under_test = "testuser1@finapi.com"
prefix = "http-user"

access_token = ""

def test_root_endpoint(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200, response.json()
    assert "detail" in response.json()
    assert response.json()["detail"] == "Welcome to finapi"

def test_create_test_user(client: TestClient, test_password: str) -> None:
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

def test_login_user(client: TestClient, test_password: str):
    user_data = {
        'username':email_under_test,
        'password':test_password
    }
    response = client.post('/token', data=user_data)

    assert response.status_code == 200, response.json()
    data = response.json()

    assert data['token_type'] == 'Bearer'
    access_token = data['access_token']
