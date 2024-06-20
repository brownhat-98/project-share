# from django import forms
# from django.forms import ModelForm
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username','first_name','last_name','email','password1','password2')
#         widgets = {
#             'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
#             'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
#             'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(CreateUserForm, self).__init__(*args, **kwargs)
#         self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your password'})
#         self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})
