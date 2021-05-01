from rest_framework import serializers

from sitraved.apps.media_api.models import MovieGenre


class MovieGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieGenre
        fields = ('name', )
