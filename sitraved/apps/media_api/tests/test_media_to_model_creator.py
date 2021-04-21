import json
import os
import responses
import pytest

from django.conf import settings

from sitraved.apps.media_api.models import Movie, MovieGenre, Language, CrewMember, MovieCrewMember
from sitraved.apps.media_api.utils.MediaToModelCreator import MediaToModelCreator

TMDB_ID_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/movie_search_by_tmdb_id.json')
CREDITS_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/movie_search_credits.json')


@pytest.mark.django_db
class TestMediaToModelCreator:

    @responses.activate
    def test_media_to_model_creator(self):
        movie_tmdb_id = 664596
        tmdb_id_data = json.load(open(TMDB_ID_SEARCH_DATA))
        credits_data = json.load(open(CREDITS_SEARCH_DATA))
        responses.add(
            responses.GET, f'https://api.themoviedb.org/3/movie/{movie_tmdb_id}?api_key={settings.TMDB_API_KEY}',
            json=tmdb_id_data, status=200)

        responses.add(
            responses.GET,
            f'https://api.themoviedb.org/3/movie/{movie_tmdb_id}/credits?api_key={settings.TMDB_API_KEY}',
            json=credits_data, status=200)

        movie = MediaToModelCreator().create_movie(movie_tmdb_id)
        assert Movie.objects.all().count() == 1
        assert Movie.objects.first().id == movie.id
        assert movie.title == 'Funny Face'
        assert movie.director.name == 'Tim Sutton'
        assert movie.genres.first().name == 'Drama'
        assert movie.language.name == 'English'

        assert MovieGenre.objects.all().count() == 1
        assert MovieGenre.objects.first().name == 'Drama'
        assert Language.objects.all().count() == 1
        assert Language.objects.first().name == 'English'

        assert CrewMember.objects.all().count() == 8
        assert CrewMember.objects.filter(name='Cosmo Jarvis').first()

        assert MovieCrewMember.objects.filter(movie=movie).count() == 7
