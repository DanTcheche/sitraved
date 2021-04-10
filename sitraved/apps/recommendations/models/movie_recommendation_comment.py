from django.db import models

from sitraved.apps.recommendations.models.comment import Comment
from sitraved.apps.recommendations.models.movie_recommendation import MovieRecommendation


class MovieRecommendationComment(Comment):
    movie_recommendation = models.ForeignKey(MovieRecommendation,
                                             related_name='comments',
                                             on_delete=models.CASCADE)
