from django.db import models
from sitraved.apps.users.models.user import BaseModel, User


class Recommendation(BaseModel):
    user = models.ForeignKey(User, related_name='recommendations', on_delete=models.CASCADE)
    description = models.Charfield(max_length=500)

    class Meta:
        abstract = True
