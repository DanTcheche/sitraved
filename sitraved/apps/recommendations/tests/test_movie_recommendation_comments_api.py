import pytest
from rest_framework.test import APIClient

from sitraved.apps.media_api.tests.factories.MovieFactory import MovieFactory
from sitraved.apps.recommendations.tests.factories.movie_recommendation_factory import MovieRecommendationFactory
from sitraved.apps.users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestMovieRecommendationCommentsViewSet:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()
        self.tmdb_id = 664596
        self.user = UserFactory(username='testuser', email='test@user.com', password='correctpassword')
        self.another_user = UserFactory(username='another_user', email='another@user.com', password='correctpassword')

    def test_create_movie_recommendation_comment(self, set_up):
        movie = MovieFactory(tmdb_id=664596, title='Funny Face')
        self.__login_user(set_up, self.user, 'correctpassword')

        MovieRecommendationFactory(movie=movie, user=self.another_user)

        params = {
            'tmdb_id': movie.tmdb_id
        }

        response = self.client.post('/api/recommendations/comments/', params)

        assert response.status_code == 200, str(response.content)
        response = response.json()
        assert response['movie_recommendation']['movie']['id'] == movie.id
        assert response['movie_recommendation']['user']['username'] == self.another_user.username
        assert response['liked']

    def test_cannot_comment_if_movie_recommendation_not_existing(self, set_up):
        movie = MovieFactory(tmdb_id=664596, title='Funny Face')
        self.__login_user(set_up, self.user, 'correctpassword')

        params = {
            'tmdb_id': movie.tmdb_id
        }

        response = self.client.post('/api/recommendations/comments/', params)

        assert response.status_code == 400, str(response.content)
        response = response.json()
        assert not response['success']
        assert response['message'] == 'You cannot add a comment to this film.'

    def test_cannot_comment_if_movie_not_existing(self, set_up):
        self.__login_user(set_up, self.user, 'correctpassword')

        params = {
            'tmdb_id': 123456
        }

        response = self.client.post('/api/recommendations/comments/', params)

        assert response.status_code == 400, str(response.content)
        response = response.json()
        assert not response['success']
        assert response['message'] == 'You cannot add a comment to this film.'

    def test_cannot_comment_twice(self, set_up):
        movie = MovieFactory(tmdb_id=664596, title='Funny Face')
        self.__login_user(set_up, self.user, 'correctpassword')

        params = {
            'tmdb_id': movie.tmdb_id
        }

        MovieRecommendationFactory(movie=movie, user=self.another_user)

        self.client.post('/api/recommendations/comments/', params)

        response = self.client.post('/api/recommendations/comments/', params)

        assert response.status_code == 400, str(response.content)
        response = response.json()
        assert not response['success']
        assert response['message'] == 'You have already recommended this movie.'

    def test_cannot_comment_if_recommended_by_self(self, set_up):
        movie = MovieFactory(tmdb_id=664596, title='Funny Face')
        self.__login_user(set_up, self.user, 'correctpassword')

        params = {
            'tmdb_id': movie.tmdb_id
        }

        MovieRecommendationFactory(movie=movie, user=self.user)

        response = self.client.post('/api/recommendations/comments/', params)

        assert response.status_code == 400, str(response.content)
        response = response.json()
        assert not response['success']
        assert response['message'] == 'You have already recommended this movie.'

    def __login_user(self, set_up, user, password):
        login_params = {
            'username': user.username,
            'password': password,
        }

        response = self.client.post('/api/users/login/', login_params)
        access_token = response.json()["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
