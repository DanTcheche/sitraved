from django.db import models

from sitraved.apps.recommendations.models import Recommendation


class Comment(Recommendation):
    liked = models.BooleanField(default=False)

    class Meta:
        abstract = True
