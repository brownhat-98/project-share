from django.forms import ModelForm,FileInput
from .models import Order,Customer
from django.contrib.auth.models import User



class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'



class EditProfileForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'profile_pic']
        widgets = {
            'profile_pic': FileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False
