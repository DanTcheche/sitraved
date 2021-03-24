import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
