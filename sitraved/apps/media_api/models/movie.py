from django.db import models

from sitraved.apps.media_api.models import MovieGenre, CrewMember, Language
from sitraved.apps.users.models.user import BaseModel


class Movie(BaseModel):
    imdb_id = models.CharField(max_length=10, blank=True, null=True, unique=True, db_index=True)
    tmdb_id = models.CharField(max_length=10, blank=True, null=True, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language, related_name='movies', blank=True, null=True, on_delete=models.SET_NULL)
    poster_url = models.CharField(max_length=255, blank=True, null=True)
    backdrop_url = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    genres = models.ManyToManyField(MovieGenre)

    director = models.ForeignKey(CrewMember, related_name='movies_directed', blank=True, null=True,
                                 on_delete=models.SET_NULL)
    year = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
