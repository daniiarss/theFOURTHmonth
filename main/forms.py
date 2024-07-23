from django.forms import ModelForm, Form
from main.models import Product
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
class UserLoginForm(Form):
    username = forms.CharField(label="Логин", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        }
    ))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        }
    ))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("User credentials were not provided.")
        return self.cleaned_data

class UserRegistrationForm(Form):
    username = forms.CharField(label="Логин",widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Enter username'
        }
    ))
    password1 = forms.CharField(label="Пароль",widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Enter Password'
        }
    ))
    password2 = forms.CharField(label="Повторите пароль",widget=forms.PasswordInput(
        attrs={'class': 'form-control',
        'placeholder':'Repeat Password'
        }
    ))

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Passwords don\'t match!')
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("User already exists!")




class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = 'sizes tittle description price' .split()
        widgets = {
            'tittle': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sizes': forms.CheckboxSelectMultiple()

        }