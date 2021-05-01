from django.urls import include, path
from rest_framework import routers

from sitraved.apps.recommendations.views.movie_recommendation_comments_views import MovieRecommendationCommentsViewSet
from sitraved.apps.recommendations.views.movie_recommendation_views import MovieRecommendationsViewSet, \
    GetUserRecommendationsMoviesIds

router = routers.SimpleRouter()
router.register(r'movies', MovieRecommendationsViewSet)
router.register(r'comments', MovieRecommendationCommentsViewSet)

urlpatterns = [  # pylint: disable=invalid-name
    path('', include(router.urls)),
    path('recommendation-movies-ids/', GetUserRecommendationsMoviesIds.as_view(), name="recommendation_movies_ids_api"),
]
