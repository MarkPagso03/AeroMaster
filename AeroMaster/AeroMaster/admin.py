from django.contrib import admin
from .models import Question, User  # Import your model

admin.site.register(Question)  # Register the model
admin.site.register(User)  # Register the model
