from django.db import models
from sitraved.apps.users.models.user import BaseModel


class Recommendation(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)

    class Meta:
        abstract = True


class Comment(Recommendation):
    liked = models.BooleanField(default=False)

    class Meta:
        abstract = True
