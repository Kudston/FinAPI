from fastapi.testclient import TestClient

test_users = ['user1@finapi.com','user2@finapi.com','user3@finapi.com','user4@finapi.com']

users_informations = {}
initial_account_info = {}

def test_create_multiple_users(client: TestClient, test_password: str):
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

def login_test(client: TestClient, test_password: str, email: str,):
    response = client.post('/token', data={
        'username':email,
        'password':test_password
    })

    assert response.status_code == 200, response.json()
    btoken = response.json()['access_token']

    return {'Authorization':f'Bearer {btoken}'}

def test_get_account_info(client: TestClient, test_password: str):
    for email in test_users:
        auth_header = login_test(client=client, test_password=test_password, email=email)
        user_id = users_informations[email]['id']
        response = client.get(f'/transactions/account-info?user_id={user_id}', headers=auth_header)

        assert response.status_code == 200, response.json()

        initial_account_info.update({email:response.json()})


def test_fund_account1(client: TestClient, test_get_admin_user_header:dict):
    user1_account_number = initial_account_info[test_users[0]]['account_number']
    
    response = client.post(f'/transactions/fund-account?account_number={user1_account_number}&amount=5000',
                           headers={
                               **test_get_admin_user_header
                               }
                        )
    
    assert response.status_code == 200, response.json()

    data = response.json()

    assert data['account_balance'] == 5000

def test_transfer_fund_to_other_accounts(client: TestClient, test_password: str):
    ##login rich user
    rich_user_header = login_test(client=client, test_password=test_password, email=test_users[0])
    rich_man_account_number = initial_account_info[test_users[0]]['account_number']

    ##sends 500 to each of his friends 
    account_no2 = initial_account_info[test_users[1]]['account_number']
    response = client.post('/transactions/send-funds',
                            json={
                            'debited_account_number': rich_man_account_number,
                            'credited_account_number': account_no2,
                            'amount': 500,
                            'note': 'Payment to friend'
                            }, headers=rich_user_header)

    assert response.status_code == 200, response.json()

    account_no3 = initial_account_info[test_users[2]]['account_number']
    response = client.post('/transactions/send-funds',
                            json={
                                'debited_account_number':rich_man_account_number,
                                'credited_account_number':account_no3,
                                'amount':500
                            }, headers=rich_user_header)

    assert response.status_code == 200, response.json()
    
    ##get user balances
    response = client.get(f'/transactions/account-info?user_id={users_informations[test_users[0]]["id"]}', 
                          headers=rich_user_header
                          )
    assert response.status_code == 200, response.json()

    assert response.json()['account_balance'] == 4000

    ##test second user
    user2_headers = login_test(client=client, test_password=test_password, email=test_users[1])
    response = client.get(f'/transactions/account-info?user_id={users_informations[test_users[1]]["id"]}',
                          headers=user2_headers)
    
    assert response.status_code == 200, response.json()

    assert response.json()['account_balance'] == 500

    ##test last user
    user3_headers = login_test(client=client, test_password=test_password, email=test_users[2])
    response = client.get(f'/transactions/account-info?user_id={users_informations[test_users[2]]["id"]}',
                          headers=user3_headers)
    
    assert response.status_code == 200, response.json()

    assert response.json()['account_balance'] == 500

