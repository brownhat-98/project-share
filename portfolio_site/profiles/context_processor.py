from django.contrib.auth.models import Group

def is_admin(request):
    is_admin = False
    if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
        is_admin = True
    return {'is_admin':is_admin}

def is_intern(request):
    is_intern = False
    if request.user.is_authenticated and request.user.groups.filter(name='Intern').exists():
        is_intern = True
    return {'is_intern':is_intern}