from django.contrib import admin
from .models import Question, User  # Import your model
from import_export.admin import ImportExportModelAdmin
from .resources import QuestionResource, UserResource


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
