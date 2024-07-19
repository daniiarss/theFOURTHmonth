from django.forms import ModelForm
from main.models import Product
from django import forms

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