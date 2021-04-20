from django.db import models

from sitraved.apps.media_api.models import CrewMember, Movie
from sitraved.apps.users.models.user import BaseModel


class MovieCrewMember(BaseModel):
    crew_member = models.ForeignKey(CrewMember, related_name='movies', blank=True, null=True,
                                    on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='crew', blank=True, null=True,
                              on_delete=models.CASCADE)
