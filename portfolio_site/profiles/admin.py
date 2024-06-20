from django.contrib import admin

# Register your models here.
from .models import UserProfile, Project, Portfolio

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Portfolio)