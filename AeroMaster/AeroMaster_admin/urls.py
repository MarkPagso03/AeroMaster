from django.urls import path
from .views import admin_view, faculty_list

urlpatterns = [
    path('', admin_view, name='AeroMaster_admin'),
    path('faculties/', faculty_list, name='faculty_list'),
]
