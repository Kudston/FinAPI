from fastapi.testclient import TestClient

test_users = ['user1@finapi.com','user2@finapi.com','user3@finapi.com','user4@finapi.com']

users_informations = {}

def test_create_users(client: TestClient, test_password: str):
    for email in test_users:
        user_data = {
        'email':email,
        'first_name':f'first{email.split("@")[0]}',
        'last_name': f'last{email.split("@")[0]}',
        'password': test_password
        }
        
        response = client.post('/users', json=user_data)
        
        assert response.status_code == 200, response.json()

        assert response.json()['email'] == email

        users_informations.update({email:response.json()})

    print(users_informations)


# def test_get_account_balance(client: TestClient, test_password: str):
#     for email in test_users:
