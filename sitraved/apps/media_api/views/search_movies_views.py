from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sitraved.apps.media_api.clients.TMDB_client import TMDBClient
from sitraved.apps.media_api.strategies.search_movies_strategy import SearchMovies


class SearchMoviesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        title = request.GET.get('title') or ''
        data = self.__search_movies(title)
        return Response(data, status=status.HTTP_200_OK)

    def __search_movies(self, title):
        movies_strategy = SearchMovies()
        tmdb_client = TMDBClient(movies_strategy)
        tmdb_response = tmdb_client.search({'title': title})
        response = self.__build_search_response(tmdb_response['movies'])
        return response

    def __build_search_response(self, movies):
        data = {'movies': []}
        for movie in movies:
            data['movies'].append({
                'id': movie['id'],
                'title': movie['title'],
                'year': movie['year'],
                'plot': movie['plot'],
                'poster_url': movie['poster_url'],
                'backdrop_url': movie['backdrop_url'],
                'tmdb_present': False
            })
        return data
