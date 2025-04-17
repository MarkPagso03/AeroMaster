from django.contrib import admin
from .models import Question, Student  # Import your model
from AeroMaster_admin.models import ExamResult, UserFeedback, faculty
from import_export.admin import ImportExportModelAdmin
from .resources import QuestionResource, UserResource, ExamResultResource, UserFeedbackResource, FacultyResource


# admin.site.register(Question)  # Register the model
# admin.site.register(User)  # Register the model


@admin.register(Question)
class Question(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer',
                    'subject')  # List the fields you want to display


@admin.register(Student)
class User(ImportExportModelAdmin):
    resource_class = UserResource
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('first_name', 'middle_initial', 'last_name', 'id_number', 'email',
                    'password')  # List the fields you want to display


@admin.register(ExamResult)
class ExamResult(ImportExportModelAdmin):
    resource_class = ExamResultResource
    list_display = ('student_id', 'aero_result', 'math_result', 'struc_result', 'acrm_result', 'pwrp_result',
                    'eemle_result', 'percent_result', 'total_result')


@admin.register(UserFeedback)
class UserFeedback(ImportExportModelAdmin):
    resource_class = UserFeedbackResource
    list_display = ('student_id', 'aero_satisfaction', 'aero_comments', 'math_satisfaction', 'math_comments',
                    'struc_satisfaction', 'struc_comments', 'acrm_satisfaction', 'acrm_comments',
                    'pwrp_satisfaction', 'pwrp_comments', 'eemle_satisfaction', 'eemle_comments')


@admin.register(faculty)
class FacultyAdmin(ImportExportModelAdmin):
    resource_class = FacultyResource
    list_display = ('first_name', 'last_name', 'emp_id', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('first_name', 'last_name', 'emp_id', 'email')
