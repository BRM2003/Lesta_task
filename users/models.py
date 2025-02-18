from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    birth_date = models.DateField()
    email = models.EmailField(unique=True)

