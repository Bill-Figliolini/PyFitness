from typing import override
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import IntegerField, TextField


# Create your models here.
class User(AbstractUser):
    """
    Class for handling the Database potion of userdata.

    Attributes:
    Methods:
    """

    id: IntegerField[int] = models.IntegerField(primary_key=True)
    name: TextField[str] = TextField()

    @override
    def __str__(self) -> str:
        return f"User {self.id}, {self.name}"
