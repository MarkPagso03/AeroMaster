from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Student  # Import your custom table model
from AeroMaster_admin.models import AeroMaster_admin, faculty


class UserBackend(BaseBackend):
    def authenticate(self, request, id_number=None, password=None, **kwargs):
        print('authenticate user')
        try:
            # Query the 'students' table for a matching ID
            student = Student.objects.get(id_number=id_number)
            # Verify the password (assuming it's hashed)
            if check_password(password, student.password):
                return student  # Return the authenticated user
        except Student.DoesNotExist:
            return None  # Return None if no user found

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None


class AeroMaster_adminBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('authen admin backend')
        # Try authenticating as admin
        try:
            print('admin try')
            admin = AeroMaster_admin.objects.get(username=username)
            if check_password(password, admin.password):
                return admin
        except AeroMaster_admin.DoesNotExist:
            pass

        # Try authenticating as faculty using emp_id as username
        try:
            print('faculty try')
            faculty_user = faculty.objects.get(emp_id=username)
            if check_password(password, faculty_user.password):
                return faculty_user
        except faculty.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return AeroMaster_admin.objects.get(pk=user_id)
        except AeroMaster_admin.DoesNotExist:
            pass

        try:
            return faculty.objects.get(pk=user_id)
        except faculty.DoesNotExist:
            return None
