from django.db import models
from sitraved.apps.users.models.user import BaseModel


class MovieGenre(BaseModel):
    tmdb_id = models.CharField(max_length=10, blank=True, null=True, unique=True, db_index=True)
    name = models.CharField(max_length=255)
