from rest_framework import serializers

from sitraved.apps.media_api.models import CrewMember


class CrewMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrewMember
        fields = ('name', )
