from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
import pytz
from django.utils import timezone


# Create your models here.

class AeroMaster_admin(models.Model):
    username = models.CharField(max_length=50, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)
    role = models.CharField(max_length=20, editable=False, default='aeromaster_admin')
    last_login = models.DateTimeField(default=now, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Explicit field for is_active
    is_staff = models.BooleanField(default=False)  # Explicit field for is_staff

    @property
    def is_authenticated(self):
        """ ✅ Required for Django authentication """
        return True

    @property
    def is_anonymous(self):
        """ ✅ Required to avoid 'is_anonymous' error """
        return False  # Custom users are never anonymous

    def save(self, *args, **kwargs):
        existing = AeroMaster_admin.objects.filter(pk=self.pk).first()
        if not existing or existing.password != self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


class faculty(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    emp_id = models.CharField(max_length=50, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)
    role = models.CharField(max_length=20, editable=False, default='faculty')
    is_active = models.BooleanField(default=True)  # Explicit field for is_active
    is_staff = models.BooleanField(default=False)  # Explicit field for is_staff

    last_login = models.DateTimeField(default=now, blank=True, null=True)

    @property
    def is_authenticated(self):
        """ ✅ Required for Django authentication """
        return True

    @property
    def is_anonymous(self):
        """ ✅ Required to avoid 'is_anonymous' error """
        return False  # Custom users are never anonymous

    def save(self, *args, **kwargs):
        if self.pk:
            # Fetch the existing faculty object only when updating
            existing = faculty.objects.filter(pk=self.pk).first()
            if existing and existing.password != self.password:
                self.password = make_password(self.password)
        else:
            # New faculty, hash the password
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ArchiveFaculty(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    emp_id = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, null=False)
    archived_at = models.DateTimeField(auto_now_add=True, null=False)
    role = models.CharField(max_length=20, editable=False, default='faculty')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ArchiveStudent(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    id_number = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, null=False)
    archived_at = models.DateTimeField(auto_now_add=True, null=False)
    role = models.CharField(max_length=20, editable=False, default='user')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ArchiveQuestion(models.Model):
    text = models.CharField(max_length=500, unique=True)
    option_a = models.CharField(max_length=255, blank=False, null=False)
    option_b = models.CharField(max_length=255, blank=False, null=False)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, blank=False, null=False)
    subject = models.CharField(max_length=50, blank=True, null=False)

    def __str__(self):
        return self.text


class GeneratedQuestions(models.Model):
    text = models.CharField(max_length=500, unique=True)
    option_a = models.CharField(max_length=255, blank=False, null=False)
    option_b = models.CharField(max_length=255, blank=False, null=False)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, blank=False, null=False)
    subject = models.CharField(max_length=50, blank=True, null=False)

    def __str__(self):
        return self.text


class ExamSetting(models.Model):
    subject = models.CharField(max_length=50, blank=False, null=False)
    date_time = models.DateTimeField(blank=False, null=False)
    passing_score = models.IntegerField(default=38)
    shuffle = models.BooleanField(default=True, blank=False, null=False)
    duration = models.IntegerField()  # Store duration in minutes

    def __str__(self):
        return f"{self.subject} - {self.date_time} - {self.duration} mins"


class ExamResult(models.Model):
    student_id = models.CharField(max_length=50, blank=False, null=False)
    aero_result = models.IntegerField(null=True, blank=True)
    math_result = models.IntegerField(null=True, blank=True)
    struc_result = models.IntegerField(null=True, blank=True)
    acrm_result = models.IntegerField(null=True, blank=True)
    pwrp_result = models.IntegerField(null=True, blank=True)
    eemle_result = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.student_id


class UserFeedback(models.Model):
    SATISFACTION_CHOICES = [
        (1, 'Dissatisfied'),
        (2, 'Satisfied'),
        (3, 'Very Satisfied'),
    ]

    student_id = models.CharField(max_length=50, blank=False, null=False)
    subject = models.CharField(max_length=100)  # optional, related to exam subject maybe?
    satisfaction = models.IntegerField(choices=SATISFACTION_CHOICES)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student_id} - {self.subject} - {self.satisfaction}"