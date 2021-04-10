from django.db import models
from sitraved.apps.users.models.user import BaseModel


class Movie(BaseModel):
    imdb_id = models.CharField(max_length=255, blank=True, null=True, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    poster_url = models.CharField(max_length=255, blank=True, null=True)
    backdrop_url = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    director = models.CharField(max_length=255, blank=True, null=True)
    raw_cast = models.CharField(max_length=5000, blank=True, null=True)
    raw_genres = models.CharField(max_length=2000, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
