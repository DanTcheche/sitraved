import factory

from sitraved.apps.media_api.models import Movie


class MovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = Movie

    id = factory.Sequence(lambda n: n + 1)
    tmdb_id = factory.Sequence(lambda n: f'tmdb_id_{n}')
    imdb_id = factory.Sequence(lambda n: f'imdb_id_{n}')
    title = factory.Sequence(lambda n: f'movie_{n}')
