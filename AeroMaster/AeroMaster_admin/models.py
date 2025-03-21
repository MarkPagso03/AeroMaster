from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.

class AeroMaster_admin(models.Model):
    username = models.CharField(max_length=50, blank=False, null=False, primary_key=True, unique=True)
    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)

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
        if not self.pk or AeroMaster_admin.objects.get(pk=self.pk).password != self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


class faculty(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    emp_id = models.CharField(max_length=50, blank=False, null=False, primary_key=True, unique=True)
    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ArchiveStudent(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    id_number = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, null=False)
    archived_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



