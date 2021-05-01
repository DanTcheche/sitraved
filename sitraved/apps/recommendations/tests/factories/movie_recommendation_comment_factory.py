import factory

from sitraved.apps.recommendations.models import MovieRecommendationComment
from sitraved.apps.recommendations.tests.factories.movie_recommendation_factory import MovieRecommendationFactory


class MovieRecommendationCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MovieRecommendationComment

    movie_recommendation = factory.SubFactory(MovieRecommendationFactory)
