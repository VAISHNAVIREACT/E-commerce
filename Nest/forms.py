from django import forms
from django.contrib.auth.models import User
from . import models
from django.core.validators import RegexValidator



class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']

class ProductForm(forms.ModelForm):
    class Meta:
        model=models.Product
        fields=['name','price','description','product_image']


class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile = forms.CharField(max_length=15, validators=[RegexValidator(r'^\d+$', 'Enter a valid mobile number.')])
    Address = forms.CharField(max_length=500)



