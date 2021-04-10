from django.db import models

from sitraved.apps.recommendations.models.recommendation import Comment


class MovieRecommendationComment(Comment):
    movie_recommendation = models.ForeignKey('MovieRecommendation',
                                             related_name='comments',
                                             on_delete=models.CASCADE)
