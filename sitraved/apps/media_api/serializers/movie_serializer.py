from rest_framework import serializers

from sitraved.apps.media_api.models import Movie
from sitraved.apps.media_api.serializers.crew_member_serializer import CrewMemberSerializer
from sitraved.apps.media_api.serializers.movie_genre_serializer import MovieGenreSerializer
from sitraved.apps.media_api.serializers.language_serializer import LanguageSerializer


class MovieSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)
    director = CrewMemberSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'plot', 'language', 'poster_url', 'backdrop_url', 'duration', 'genres', 'director',
                  'year', 'slug')
