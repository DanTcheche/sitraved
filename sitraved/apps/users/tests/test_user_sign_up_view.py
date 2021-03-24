import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserSignUpView:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()

    def test_user_correct_sign_up(self, set_up):
        params = {
            'username': 'TestUser',
            'email': 'test@user.com',
            'password': 'asdasdasd',
            'password_confirmation': 'asdasdasd',
        }
        response = self.client.post('/api/users/register/', params)

        assert response.status_code == 200, str(response.content)
        response = response.json()
        assert response['success']
        user = response['user']
        assert user['username'] == 'TestUser'
        assert user['email'] == 'test@user.com'
        assert 'refresh_token' in response
        assert 'access_token' in response
