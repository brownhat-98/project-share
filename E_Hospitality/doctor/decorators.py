from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda user: user.groups.filter(name='Admin').exists())(view_func))
    return decorated_view_func