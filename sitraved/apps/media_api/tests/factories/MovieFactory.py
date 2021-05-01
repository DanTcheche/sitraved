import factory

from sitraved.apps.media_api.models import Movie


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    id = factory.Sequence(lambda n: f'00000000-0000-0000-0000-00000000000{n + 1}')
    tmdb_id = factory.Sequence(lambda n: f'tmdb_id_{n}')
    imdb_id = factory.Sequence(lambda n: f'imdb_id_{n}')
    title = factory.Sequence(lambda n: f'movie_{n}')
