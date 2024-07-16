def user_roles(request):
    roles = {
        'is_admin': False,
        'is_doctor': False,
        'is_patient': False,
    }
    if request.user.is_authenticated:
        user = request.user
        roles['is_admin'] = user.groups.filter(name='Admin').exists()
        roles['is_doctor'] = user.groups.filter(name='Doctor').exists()
        roles['is_patient'] = user.groups.filter(name='Patient').exists()
    return {'user_roles': roles}
