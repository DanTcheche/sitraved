from rest_framework import serializers

from sitraved.apps.recommendations.models import MovieRecommendationComment
from sitraved.apps.recommendations.serializers.movie_recommendation_serializer import MovieRecommendationSerializer


class MovieRecommendationCommentSerializer(serializers.ModelSerializer):
    movie_recommendation = MovieRecommendationSerializer()

    class Meta:
        model = MovieRecommendationComment
        fields = ('movie_recommendation', 'liked')
