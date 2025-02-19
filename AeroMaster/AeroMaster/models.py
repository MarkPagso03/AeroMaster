from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz
from django.utils.timezone import now


def current_time_utc_plus_8():
    local_timezone = pytz.timezone("Asia/Manila")  # Change to your local timezone
    local_time = now().astimezone(local_timezone)
    clean_local_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
    return clean_local_time


class User(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    id_number = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)

    last_login = models.DateTimeField(default=now, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} + {self.last_name}"
