from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=('categories', 'title', 'description', 'price', 'photo',)
        widgets = {
            'category': forms.Select(attrs={
                'class': 'mb-3'
            })
        }