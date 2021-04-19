from django.urls import include, path
from rest_framework import routers

from sitraved.apps.recommendations.views.movie_recommendation_views import MovieRecommendationsViewSet

router = routers.SimpleRouter()
router.register(r'movies', MovieRecommendationsViewSet)

urlpatterns = [  # pylint: disable=invalid-name
    path('', include(router.urls)),
]