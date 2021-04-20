from django.db import models
from sitraved.apps.users.models.user import BaseModel


class Language(BaseModel):
    name = models.CharField(max_length=255)
    iso_639_1 = models.CharField(max_length=2, blank=True, null=True, unique=True)
