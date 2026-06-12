from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import *

admin.site.register(Department)
admin.site.register(User, UserAdmin)
admin.site.register(Asset)
admin.site.register(Project)
admin.site.register(Organization)
admin.site.register(MaintenanceLog)  # Assignment 2
