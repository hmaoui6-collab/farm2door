from django import forms
from django.contrib.auth.models import User
from .models import Product


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[('customer', 'Client'), ('farmer', 'Agriculteur')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'image']
