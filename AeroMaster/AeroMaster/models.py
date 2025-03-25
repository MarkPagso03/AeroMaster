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
    id_number = models.CharField(max_length=50, blank=False, null=False, primary_key=True)
    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)
    role = models.CharField(max_length=20, editable=False, default='user')
    last_login = models.DateTimeField(default=now, blank=True, null=True)

    @property
    def is_authenticated(self):
        """ ✅ Required for Django authentication """
        return True

    @property
    def is_anonymous(self):
        """ ✅ Required to avoid 'is_anonymous' error """
        return False  # Custom users are never anonymous

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Question(models.Model):
    text = models.CharField(max_length=500, unique=True)
    option_a = models.CharField(max_length=255, blank=False, null=False)
    option_b = models.CharField(max_length=255, blank=False, null=False)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, blank=False, null=False)
    subject = models.CharField(max_length=50, blank=True, null=False)

    def __str__(self):
        return self.text
