import factory

from sitraved.apps.media_api.tests.factories.MovieFactory import MovieFactory
from sitraved.apps.recommendations.models import MovieRecommendation


class MovieRecommendationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MovieRecommendation

    movie = factory.SubFactory(MovieFactory)
