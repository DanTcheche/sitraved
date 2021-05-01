from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sitraved.apps.media_api.clients.TMDB_client import TMDBClient
from sitraved.apps.media_api.strategies.search_movies_strategy import SearchMovies
from sitraved.apps.recommendations.models import MovieRecommendation, MovieRecommendationComment


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
            already_recommended_by = None
            movie_recommendation = MovieRecommendation.objects.filter(movie__tmdb_id=movie['id'])
            if movie_recommendation.exists():
                movie_comment_recommendation = MovieRecommendationComment.objects.filter(
                    movie_recommendation=movie_recommendation.first(), user=self.request.user
                )
                already_recommended_by = movie_recommendation.filter(user=self.request.user).exists() or \
                    movie_comment_recommendation.exists()
            data['movies'].append({
                'id': movie['id'],
                'title': movie['title'],
                'year': movie['year'],
                'plot': movie['plot'],
                'poster_url': movie['poster_url'],
                'backdrop_url': movie['backdrop_url'],
                'tmdb_present': False,
                'already_recommended_by': already_recommended_by
            })
        return data
