from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sitraved.apps.media_api.models import Movie
from sitraved.apps.media_api.utils.MediaToModelCreator import MediaToModelCreator
from sitraved.apps.recommendations.models import MovieRecommendation
from sitraved.apps.recommendations.serializers.movie_recommendation_serializer import MovieRecommendationSerializer


class MovieRecommendationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MovieRecommendation.objects.all()
    serializer_class = MovieRecommendationSerializer

    def create(self, request):
        tmdb_id = request.data.get('tmdb_id')
        description = request.data.get('description')
        movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
        if not movie:
            movie = MediaToModelCreator().create_movie(tmdb_id)
        movie_recommendation = MovieRecommendation.objects.filter(user=request.user, movie=movie).first()
        if movie_recommendation:
            return Response({'success': False, 'message': 'You have already recommended this movie.'},
                            status=status.HTTP_400_BAD_REQUEST)

        movie_recommendation = MovieRecommendation.objects.create(user=request.user, movie=movie,
                                                                  description=description)
        return Response(movie_recommendation, status=status.HTTP_200_OK)
