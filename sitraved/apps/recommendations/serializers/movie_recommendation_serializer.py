from rest_framework import serializers

from sitraved.apps.media_api.serializers.movie_serializer import MovieSerializer
from sitraved.apps.recommendations.models import MovieRecommendation
from sitraved.apps.users.serializers.user_serializers import UserModelSerializer


class MovieRecommendationSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    user = UserModelSerializer()

    class Meta:
        model = MovieRecommendation
        fields = ('movie', 'user', 'description')
