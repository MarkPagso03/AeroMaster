from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    id_number = models.CharField(max_length=20, unique=True)
