import pytest
from rest_framework.test import APIClient

from sitraved.apps.users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestUserLoginView:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()

    def test_user_correct_login(self, set_up):
        UserFactory(username='testuser', email='test@user.com', password='correctpassword')

        login_params = {
            'username': 'TestUser',
            'password': 'correctpassword',
        }
        response = self.client.post('/api/users/login/', login_params)

        assert response.status_code == 200, str(response.content)
        response = response.json()
        assert response['success']
        user = response['user']
        assert user['username'] == 'testuser'
        assert user['email'] == 'test@user.com'
        assert 'refresh_token' in response
        assert 'access_token' in response

    def test_user_incorrect_password_login(self, set_up):
        UserFactory(username='TestUser', email='test@user.com', password='correctpassword')
        login_params = {
            'username': 'TestUser',
            'password': 'incorrectpassword',
        }
        response = self.client.post('/api/users/login/', login_params)

        assert response.status_code == 400, str(response.content)
        assert response.json()['non_field_errors'] == ['Invalid user or password']

    def test_user_incorrect_user_login(self, set_up):
        login_params = {
            'username': 'TestUser',
            'password': 'incorrectpassword',
        }
        response = self.client.post('/api/users/login/', login_params)

        assert response.status_code == 400, str(response.content)
        assert response.json()['non_field_errors'] == ['Invalid user or password']
