from django.contrib import admin

# Register your models here.
from .models import faculty, AeroMaster_admin, ArchiveFaculty, GeneratedQuestions, ExamSetting, ExamResult


class Role(admin.ModelAdmin):
    readonly_fields = ('role',)


admin.site.register(faculty, Role)
admin.site.register(AeroMaster_admin, Role)
admin.site.register(ArchiveFaculty, Role)
admin.site.register(GeneratedQuestions)
admin.site.register(ExamSetting)
admin.site.register(ExamResult)
