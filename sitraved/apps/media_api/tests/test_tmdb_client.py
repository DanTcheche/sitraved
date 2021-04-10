import json
import os
import responses
import pytest

from django.conf import settings

from sitraved.apps.media_api.clients.TMDB_client import TMDBClient
from sitraved.apps.media_api.strategies.search_movies_strategy import SearchMovies
from sitraved.apps.media_api.strategies.search_tv_series_strategy import SearchTVSeries

MOVIES_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/movie_search_by_title.json')
TV_SEARCH_DATA = os.path.join(os.path.dirname(__file__), 'mock_data/tv_series_search_by_title.json')


@pytest.mark.django_db
class TestTMDBClient:

    @responses.activate
    def test_search_movies_by_title(self):
        movies_strategy = SearchMovies()
        tmdb_client = TMDBClient(movies_strategy)

        response_data = json.load(open(MOVIES_SEARCH_DATA))
        responses.add(
            responses.GET, f'https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query=funny',
            json=response_data, status=200)

        response = tmdb_client.search({
            'title': 'funny'
        })

        assert len(response['movies']) == 20
        assert response['movies'][0]['title'] == 'Funny Face'
        assert response['movies'][0]['year'] == '2021'
        poster_url = 'http://image.tmdb.org/t/p/original/fD2ZAcCt4BEhKGpTxdBFoSRCn1Y.jpg'
        assert response['movies'][0]['poster_url'] == poster_url

    @responses.activate
    def test_search_tv_series_by_title(self):
        tv_series_strategy = SearchTVSeries()
        tmdb_client = TMDBClient(tv_series_strategy)

        response_data = json.load(open(TV_SEARCH_DATA))
        responses.add(
            responses.GET, f'https://api.themoviedb.org/3/search/tv?api_key={settings.TMDB_API_KEY}&query=funny',
            json=response_data, status=200)

        response = tmdb_client.search({
            'title': 'funny'
        })

        assert len(response['series']) == 20
        assert response['series'][0]['title'] == 'Funny or Die Presents'
        assert response['series'][0]['year'] == '2010'
        poster_url = 'http://image.tmdb.org/t/p/original/p1PaO1kMsLNkkw15zWsp97KN4Ez.jpg'
        assert response['series'][0]['poster_url'] == poster_url
