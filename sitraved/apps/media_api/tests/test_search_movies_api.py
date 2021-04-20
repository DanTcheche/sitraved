import pytest
import json
import os
import responses
from rest_framework.test import APIClient
from django.conf import settings

from sitraved.apps.users.tests.factories.user_factory import UserFactory

MOVIES_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/movie_search_by_title.json')


@pytest.mark.django_db
class TestSearchMoviesAPI:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()

    def test_search_movies(self, set_up):

        self.__login(set_up)

        search_params = {
            'title': 'funny',
        }

        response_data = json.load(open(MOVIES_SEARCH_DATA))
        responses.add(
            responses.GET, f'https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query=funny',
            json=response_data, status=200)

        response = self.client.get('/api/media/search/', search_params)

        print(response.json())

        assert response.status_code == 200, str(response.content)
        response = response.json()
        assert len(response['movies']) == 15
        assert 'id' in response['movies'][0]
        assert 'year' in response['movies'][0]

    def __login(self, set_up):
        UserFactory(username='testuser', email='test@user.com', password='correctpassword')

        login_params = {
            'username': 'TestUser',
            'password': 'correctpassword',
        }

        response = self.client.post('/api/users/login/', login_params)

        access_token = response.json()["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
