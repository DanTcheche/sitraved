import pytest
import json
import os
import responses
from rest_framework.test import APIClient
from django.conf import settings

from sitraved.apps.media_api.tests.factories.MovieFactory import MovieFactory
from sitraved.apps.recommendations.tests.common import login_user
from sitraved.apps.recommendations.tests.factories.movie_recommendation_comment_factory import \
    MovieRecommendationCommentFactory
from sitraved.apps.recommendations.tests.factories.movie_recommendation_factory import MovieRecommendationFactory
from sitraved.apps.users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestMovieRecommendationsFilters:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()
        self.tmdb_id = 664596
        self.user = UserFactory(username='testuser', email='test@user.com', password='correctpassword')
        self.user2 = UserFactory(username='testuser2', email='test2@user.com', password='correctpassword')
        self.user3 = UserFactory(username='testuser3', email='test3@user.com', password='correctpassword')
        self.user4 = UserFactory(username='testuser4', email='test4@user.com', password='correctpassword')
        self.user5 = UserFactory(username='testuser5', email='test5@user.com', password='correctpassword')

    def test_popularity_order(self, set_up):
        funny_face_movie = MovieFactory(tmdb_id=664596, title='Funny Face')
        joker_movie = MovieFactory(tmdb_id=475557, title='Joker')
        movie_recommendation_funny_face = MovieRecommendationFactory(movie=funny_face_movie, user=self.user)
        movie_recommendation_joker = MovieRecommendationFactory(movie=joker_movie, user=self.user)

        MovieRecommendationCommentFactory(movie_recommendation=movie_recommendation_funny_face, user=self.user2)
        MovieRecommendationCommentFactory(movie_recommendation=movie_recommendation_funny_face, user=self.user3)
        MovieRecommendationCommentFactory(movie_recommendation=movie_recommendation_funny_face, user=self.user4)
        MovieRecommendationCommentFactory(movie_recommendation=movie_recommendation_joker, user=self.user2)
        login_user(self.user, 'correctpassword', self.client)

        #   Funny face is the most recommended
        response = self.client.get('/api/recommendations/movies/?sort=popularity')

        recommendations = response.json()['results']
        assert recommendations[0]['movie']['id'] == funny_face_movie.id

        MovieRecommendationCommentFactory(movie_recommendation=movie_recommendation_joker, user=self.user3)
        MovieRecommendationCommentFactory(movie_recommendation=movie_recommendation_joker, user=self.user4)
        MovieRecommendationCommentFactory(movie_recommendation=movie_recommendation_joker, user=self.user5)

        #   Now Joker is the most recommended
        response = self.client.get('/api/recommendations/movies/?sort=popularity')

        recommendations = response.json()['results']
        assert recommendations[0]['movie']['id'] == joker_movie.id
