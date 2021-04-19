from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sitraved.apps.media_api.models import Movie
from sitraved.apps.media_api.utils.MediaToModelCreator import MediaToModelCreator
from sitraved.apps.recommendations.models import MovieRecommendation


class MovieRecommendationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MovieRecommendation.objects.all()

    def create(self, request):
        tmdb_id = request.data.get('tmdb_id')
        movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
        if not movie:
            movie = MediaToModelCreator().create_movie(tmdb_id)
        return Response(movie, status=status.HTTP_200_OK)
