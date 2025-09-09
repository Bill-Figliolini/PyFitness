from typing import override
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import OneToOneField


# Create your models here.
class UserAccount(models.Model):
    """
    Class for handling the Database potion of userdata.

    Attributes:
    Methods:
    """

    account_binding: OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    name: TextField[str] = TextField()

    @override
    def __str__(self) -> str:
        return f"User {self.account_binding}"
