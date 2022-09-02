from email.policy import default
from django import forms

from . models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'name','category','price','digital','description','image']
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),            
            'digital': '',
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name' : 'Enter Product Name:',
            'category': 'Select Category: ',
            'price': 'Enter a price: ',  
            'digital': 'Enter a Digital: ',
            'description': 'Enter product description',
            'image': 'Select an Image: ',
        }

    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [ 'name',]
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        labels = {
            'name' : 'Enter Product Name:',
            
        }  