from django.db import models

from sitraved.apps.recommendations.models import Recommendation


class MovieRecommendation(Recommendation):
    movie = models.ForeignKey('media_api.Movie', related_name='recommendations', on_delete=models.CASCADE)
