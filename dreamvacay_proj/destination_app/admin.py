from django.contrib import admin
from .models import UserProfile, Destination, Dest_Images

admin.site.register(UserProfile)
admin.site.register(Destination)
admin.site.register(Dest_Images)