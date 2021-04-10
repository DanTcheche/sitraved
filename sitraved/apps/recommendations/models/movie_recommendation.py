from django.db import models

from sitraved.apps.media_api.models import Movie
from sitraved.apps.recommendations.models import Recommendation


class MovieRecommendation(Recommendation):
    movie = models.ForeignKey(Movie, related_name='recommendations', on_delete=models.CASCADE)
