from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import User  # Import your custom table model


class UserBackend(BaseBackend):
    def authenticate(self, request, id_number=None, password=None, **kwargs):
        try:
            # Query the 'students' table for a matching ID
            student = User.objects.get(id_number=id_number)

            # Verify the password (assuming it's hashed)
            if check_password(password, student.password):
                return student  # Return the authenticated user
        except User.DoesNotExist:
            return None  # Return None if no user found

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
