from django.urls import path
from sitraved.apps.media_api.views.search_movies_views import SearchMoviesAPI

urlpatterns = [  # pylint: disable=invalid-name
    path('search/', SearchMoviesAPI.as_view(), name="search_movies_api"),
]
