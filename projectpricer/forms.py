from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    

    class Meta:
        model = Product
        exclude = ['name','last_updated','price','ean','asin','upc','currency','url']
