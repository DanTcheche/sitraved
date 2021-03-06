from django.urls import include, path
from rest_framework import routers

from sitraved.apps.recommendations.views.movie_recommendation_comments_views import MovieRecommendationCommentsViewSet
from sitraved.apps.recommendations.views.movie_recommendation_views import MovieRecommendationsViewSet

router = routers.SimpleRouter()
router.register(r'movies', MovieRecommendationsViewSet, basename='movie_recommendations')
router.register(r'comments', MovieRecommendationCommentsViewSet, basename='movie_recommendations_comments')

urlpatterns = [  # pylint: disable=invalid-name
    path('', include(router.urls)),
]
