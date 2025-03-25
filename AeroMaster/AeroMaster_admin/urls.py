from django.urls import path
from .views import (admin_view, faculty_list, edit_faculty, archive_faculty, add_faculty,
                    student_list, edit_student, archive_student, add_student,
                    login_admin_view)

urlpatterns = [
    path('', admin_view, name='AeroMaster_admin'),
    path('faculty/view', faculty_list, name='faculty_list'),
    path('faculty/add/', add_faculty, name='add_faculty'),
    path('faculty/edit/<str:faculty_id>/', edit_faculty, name='edit_faculty'),
    path('faculty/delete/<str:faculty_id>/', archive_faculty, name='archive_faculty'),
    path('student/view', student_list, name='student_list'),
    path('student/add/', add_student, name='add_student'),
    path('student/edit/<str:student_id>/', edit_student, name='edit_student'),
    path('student/delete/<str:student_id>/', archive_student, name='archive_student'),
    path('login/', login_admin_view, name='login_admin'),
    path('login/', views.login_view, name='login'),
]
