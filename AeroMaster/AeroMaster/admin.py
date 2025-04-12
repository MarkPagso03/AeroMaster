from django.contrib import admin
from .models import Question, User  # Import your model
from AeroMaster_admin.models import ExamResult, UserFeedback
from import_export.admin import ImportExportModelAdmin
from .resources import QuestionResource, UserResource, ExamResultResource, UserFeedbackResource


# admin.site.register(Question)  # Register the model
# admin.site.register(User)  # Register the model


@admin.register(Question)
class Question(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer',
                    'subject')  # List the fields you want to display


@admin.register(User)
class User(ImportExportModelAdmin):
    resource_class = UserResource
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
