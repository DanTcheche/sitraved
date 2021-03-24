import pytest
from rest_framework.test import APIClient

from sitraved.apps.users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestUserLoginView:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()

    def test_user_correct_logout(self, set_up):
        UserFactory(username='TestUser', email='test@user.com', password='correctpassword')

        login_params = {
            'username': 'TestUser',
            'password': 'correctpassword',
        }
        response = self.client.post('/api/users/login/', login_params)
        assert response.status_code == 200, str(response.content)
        access_token = response.json()["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post('/api/users/logout/')
        assert response.status_code == 200, str(response.content)

    def test_user_incorrect_logout(self, set_up):
        response = self.client.post('/api/users/logout/')
        assert response.status_code == 400, str(response.content)
