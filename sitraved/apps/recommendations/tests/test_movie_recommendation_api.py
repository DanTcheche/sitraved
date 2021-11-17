import pytest
import json
import os
import responses
from rest_framework.test import APIClient
from django.conf import settings

from sitraved.apps.media_api.tests.factories.MovieFactory import MovieFactory
from sitraved.apps.recommendations.models import MovieRecommendation
from sitraved.apps.recommendations.tests.common import login_user
from sitraved.apps.recommendations.tests.factories.movie_recommendation_factory import MovieRecommendationFactory
from sitraved.apps.users.tests.factories.user_factory import UserFactory


TMDB_ID_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/movie_search_by_tmdb_id.json')
CREDITS_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/movie_search_credits.json')


@pytest.mark.django_db
class TestMovieRecommendationsViewSet:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()
        self.tmdb_id = 664596
        self.user = UserFactory(username='testuser', email='test@user.com', password='correctpassword')

    def test_create_movie_recommendation(self, set_up):
        login_user(self.user, 'correctpassword', self.client)

        self.__set_up_data(self.tmdb_id)
        params = {
            'tmdb_id': self.tmdb_id
        }
        response = self.client.post('/api/recommendations/movies/', params)

        assert response.status_code == 200, str(response.content)
        response = response.json()
        assert response['movie']['title'] == 'Funny Face'
        assert MovieRecommendation.objects.all().count() == 1

    def test_cannot_create_same_recommendation_twice(self, set_up):
        movie = MovieFactory(tmdb_id=664596, title='Funny Face')
        login_user(self.user, 'correctpassword', self.client)

        self.__set_up_data(movie.tmdb_id)

        MovieRecommendationFactory(movie=movie, user=self.user)

        params = {
            'tmdb_id': movie.tmdb_id
        }

        response = self.client.post('/api/recommendations/movies/', params)

        assert response.status_code == 400, str(response.content)
        response = response.json()
        assert not response['success']
        assert response['message'] == 'You have already recommended this movie.'

    def test__cannot_create_movie_recommendation_not_logged_in(self, set_up):
        self.__set_up_data(self.tmdb_id)
        params = {
            'tmdb_id': self.tmdb_id
        }
        response = self.client.post('/api/recommendations/movies/', params)

        assert response.status_code == 401, str(response.content)

    def test_cannot_delete_recommendation(self, set_up):
        movie = MovieFactory(tmdb_id=664596, title='Funny Face')
        anotherUser = UserFactory(username='another_user', email='another_user@user.com', password='correctpassword')
        login_user(self.user, 'correctpassword', self.client)

        movie_recommendation = MovieRecommendationFactory(movie=movie, user=anotherUser)

        response = self.client.delete(f'/api/recommendations/movies/{movie_recommendation.id}/')

        assert response.status_code == 405, str(response.content)

    def test_cannot_edit_recommendation(self, set_up):
        movie = MovieFactory(tmdb_id=664596, title='Funny Face')
        anotherUser = UserFactory(username='another_user', email='another_user@user.com', password='correctpassword')
        login_user(self.user, 'correctpassword', self.client)

        movie_recommendation = MovieRecommendationFactory(movie=movie, user=anotherUser)
        params = {
            'description': 'New description'
        }

        response = self.client.put(f'/api/recommendations/movies/{movie_recommendation.id}/', params)

        assert response.status_code == 405, str(response.content)

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
