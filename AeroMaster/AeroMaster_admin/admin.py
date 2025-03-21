from django.contrib import admin

# Register your models here.
from .models import faculty, AeroMaster_admin, ArchiveFaculty


admin.site.register(faculty)
admin.site.register(AeroMaster_admin)
admin.site.register(ArchiveFaculty)