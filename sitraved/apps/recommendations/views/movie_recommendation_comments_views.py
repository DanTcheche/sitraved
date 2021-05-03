from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sitraved.apps.media_api.models import Movie
from sitraved.apps.recommendations.models import MovieRecommendation, MovieRecommendationComment
from sitraved.apps.recommendations.permissions.user_item_permissions import IsOwnerOrReadOnly
from sitraved.apps.recommendations.serializers.movie_recommendation_comment_serializer import \
    MovieRecommendationCommentSerializer
from sitraved.apps.recommendations.views.movie_recommendation_views import StandardResultsSetPagination


class MovieRecommendationCommentsViewSet(viewsets.ModelViewSet):
    queryset = MovieRecommendationComment.objects.all().order_by('-created_at')
    serializer_class = MovieRecommendationCommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def create(self, request):
        tmdb_id = request.data.get('tmdb_id')
        description = request.data.get('description')
        movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
        if not movie:
            return Response({'success': False, 'message': 'You cannot add a comment to this film.'},
                            status=status.HTTP_400_BAD_REQUEST)
        movie_recommendation = MovieRecommendation.objects.filter(movie=movie)
        if movie_recommendation.exists():
            movie_already_recommended_by_user = MovieRecommendationComment.objects.filter(
                    user=request.user, movie_recommendation=movie_recommendation.first()).exists() or \
                                                movie_recommendation.filter(user=request.user).exists()
            if movie_already_recommended_by_user:
                return Response({'success': False, 'message': 'You have already recommended this movie.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                movie_recommendation_comment = MovieRecommendationComment.objects.create(
                    user=request.user, description=description, liked=True,
                    movie_recommendation=movie_recommendation.first())
        else:
            return Response({'success': False, 'message': 'You cannot add a comment to this film.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(movie_recommendation_comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
