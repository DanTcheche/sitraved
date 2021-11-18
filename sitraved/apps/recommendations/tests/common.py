def login_user(user, password, client):
    login_params = {
        'username': user.username,
        'password': password,
    }

    response = client.post('/api/users/login/', login_params)
    access_token = response.json()["access_token"]
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
