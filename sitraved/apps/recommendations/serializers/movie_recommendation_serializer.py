from rest_framework import serializers

from sitraved.apps.media_api.serializers.movie_serializer import MovieSerializer
from sitraved.apps.recommendations.models import MovieRecommendation, MovieRecommendationComment
from sitraved.apps.users.serializers.user_serializers import UserModelSerializer


class MovieRecommendationSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    user = UserModelSerializer()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = MovieRecommendation
        fields = ('id', 'movie', 'user', 'description', 'comment')

    def get_comment(self, movie_recommendation):
        request = self.context.get('request', None)
        user = None
        if request:
            user = request.user
        if user and not user.is_anonymous:
            comment = MovieRecommendationComment.objects.filter(user=user,
                                                                movie_recommendation=movie_recommendation).first()
            if comment:
                return comment.id
        return None
