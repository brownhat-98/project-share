from django.forms import ModelForm,FileInput,TextInput,EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','email','phone', 'profile_pic']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'profile_pic': FileInput(attrs={'class': 'form-control'}),
        }        
        
class EditProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone', 'profile_pic']
        widgets = {
            'profile_pic': FileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False


class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'  

class DestImageForm(ModelForm):

    class Meta:
        model = Dest_Images
        fields = ['images']