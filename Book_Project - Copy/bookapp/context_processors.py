
from django.contrib.auth.models import Group

def is_admin(request):
    is_admin = False
    if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
        is_admin = True
    return {'is_admin':is_admin}