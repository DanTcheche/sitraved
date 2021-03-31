import pytest
from rest_framework.test import APIClient

from sitraved.apps.users.models import User
from sitraved.apps.users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestUserSignUpView:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()

    def test_user_correct_sign_up(self, set_up):
        params = {
            'username': 'TestUser',
            'email': 'test@user.com',
            'password': 'correctpassword',
            'password_confirmation': 'correctpassword',
        }
        response = self.client.post('/api/users/register/', params)

        assert response.status_code == 200, str(response.content)
        assert User.objects.all().count() == 1
        response = response.json()
        assert response['success']
        user = response['user']
        assert user['username'] == 'TestUser'
        assert user['email'] == 'test@user.com'
        assert 'refresh_token' in response
        assert 'access_token' in response

    def test_user_sign_up_not_matching_passwords(self, set_up):
        params = {
            'username': 'TestUser',
            'email': 'test@user.com',
            'password': 'correctpassword',
            'password_confirmation': 'incorrectpassword',
        }
        response = self.client.post('/api/users/register/', params)
        assert User.objects.all().count() == 0
        assert response.status_code == 400, str(response.content)
        assert response.json()['non_field_errors'] == ['Passwords do not match']

    def test_user_sign_up_missing_username(self, set_up):
        params = {
            'email': 'test@user.com',
            'password': 'correctpassword',
            'password_confirmation': 'correctpassword',
        }
        response = self.client.post('/api/users/register/', params)
        assert response.status_code == 400, str(response.content)
        assert response.json()['username'] == ['This field is required.']

    def test_user_sign_up_missing_email(self, set_up):
        params = {
            'username': 'TestUser',
            'password': 'correctpassword',
            'password_confirmation': 'correctpassword',
        }
        response = self.client.post('/api/users/register/', params)
        assert response.status_code == 400, str(response.content)
        assert response.json()['email'] == ['This field is required.']

    def test_user_sign_up_missing_password(self, set_up):
        params = {
            'username': 'TestUser',
            'email': 'test@user.com',
            'password_confirmation': 'correctpassword',
        }
        response = self.client.post('/api/users/register/', params)
        assert response.status_code == 400, str(response.content)
        assert response.json()['password'] == ['This field is required.']

    def test_user_sign_up_existing_username(self, set_up):
        UserFactory(username='TestUser')
        params = {
            'username': 'TestUser',
            'email': 'test@user.com',
            'password': 'correctpassword',
            'password_confirmation': 'correctpassword',
        }
        response = self.client.post('/api/users/register/', params)
        assert response.status_code == 400, str(response.content)
        assert not response.json()['success']
        assert response.json()['message'] == "An user with that username already exists."

    def test_user_sign_up_existing_email(self, set_up):
        UserFactory(email='test@user.com')
        params = {
            'username': 'TestUser',
            'email': 'test@user.com',
            'password': 'correctpassword',
            'password_confirmation': 'correctpassword',
        }
        response = self.client.post('/api/users/register/', params)
        assert response.status_code == 400, str(response.content)
        assert not response.json()['success']
        assert response.json()['message'] == "An user with that email already exists."
