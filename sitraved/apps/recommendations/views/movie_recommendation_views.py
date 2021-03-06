from django.db.models import Count

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from sitraved.apps.media_api.models import Movie
from sitraved.apps.media_api.utils.MediaToModelCreator import MediaToModelCreator
from sitraved.apps.recommendations.models import MovieRecommendation, MovieRecommendationComment
from sitraved.apps.recommendations.permissions.user_item_permissions import IsOwnerOrReadOnly
from sitraved.apps.recommendations.serializers.movie_recommendation_serializer import MovieRecommendationSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = 'page_size'


class MovieRecommendationsViewSet(viewsets.ModelViewSet):
    serializer_class = MovieRecommendationSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def get_queryset(self):
        sort = self.request.GET.get('sort', None)
        if sort and sort == 'popularity':
            return MovieRecommendation.objects.all().annotate(comments_count=Count('comments')).\
                order_by('-comments_count')
        return MovieRecommendation.objects.all().order_by('-created_at')

    def create(self, request):
        tmdb_id = request.data.get('tmdb_id')
        description = request.data.get('description')
        movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
        if not movie:
            movie = MediaToModelCreator().create_movie(tmdb_id)
        movie_recommendation = MovieRecommendation.objects.filter(movie=movie)
        if movie_recommendation.exists():
            if movie_recommendation.filter(user=request.user).exists():
                return Response({'success': False, 'message': 'You have already recommended this movie.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success': False, 'message': 'This movie was already recommended by someone else.'},
                                status=status.HTTP_400_BAD_REQUEST)

        movie_recommendation = MovieRecommendation.objects.create(user=request.user, movie=movie,
                                                                  description=description)
        serializer = self.get_serializer(movie_recommendation)
        return Response(serializer.data, status=status.HTTP_200_OK)
