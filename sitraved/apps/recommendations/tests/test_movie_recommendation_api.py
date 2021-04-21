import pytest
import json
import os
import responses
from rest_framework.test import APIClient
from django.conf import settings

from sitraved.apps.recommendations.models import MovieRecommendation
from sitraved.apps.users.tests.factories.user_factory import UserFactory


TMDB_ID_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/movie_search_by_tmdb_id.json')
CREDITS_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/movie_search_credits.json')


@pytest.mark.django_db
class TestMovieRecommendationViewSet:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()

    def test_create_movie_recommendation(self, set_up):

        self.__login(set_up)

        movie_tmdb_id = 664596

        self.__set_up_data(movie_tmdb_id)
        params = {
            'tmdb_id': movie_tmdb_id
        }
        response = self.client.post('/api/recommendations/movies/', params)

        assert response.status_code == 200, str(response.content)
        response = response.json()
        assert response['movie']['title'] == 'Funny Face'
        assert MovieRecommendation.objects.all().count() == 1

    def test_cannot_create_same_recommendation_twice(self, set_up):

        self.__login(set_up)

        movie_tmdb_id = 664596

        self.__set_up_data(movie_tmdb_id)
        params = {
            'tmdb_id': movie_tmdb_id
        }
        self.client.post('/api/recommendations/movies/', params)

        response = self.client.post('/api/recommendations/movies/', params)

        assert response.status_code == 400, str(response.content)
        response = response.json()
        assert not response['success']
        assert response['message'] == 'You have already recommended this movie.'

    def __login(self, set_up):
        UserFactory(username='testuser', email='test@user.com', password='correctpassword')

        login_params = {
            'username': 'TestUser',
            'password': 'correctpassword',
        }

        response = self.client.post('/api/users/login/', login_params)

        access_token = response.json()["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def __set_up_data(self, movie_tmdb_id):

        tmdb_id_data = json.load(open(TMDB_ID_SEARCH_DATA))
        credits_data = json.load(open(CREDITS_SEARCH_DATA))
        responses.add(
            responses.GET, f'https://api.themoviedb.org/3/movie/{movie_tmdb_id}?api_key={settings.TMDB_API_KEY}',
            json=tmdb_id_data, status=200)

        responses.add(
            responses.GET,
            f'https://api.themoviedb.org/3/movie/{movie_tmdb_id}/credits?api_key={settings.TMDB_API_KEY}',
            json=credits_data, status=200)

