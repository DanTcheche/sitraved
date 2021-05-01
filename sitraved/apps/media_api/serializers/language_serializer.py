from rest_framework import serializers

from sitraved.apps.media_api.models import Language


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('name', 'iso_639_1')
