from django import forms
from django.contrib.auth.models import User
from store.models import Customer,Product   
from django.contrib.auth.forms import UserCreationForm 
from . models import GuestUser,StoreOwner


class ResgisterUserForm(UserCreationForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    first_name=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    

    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')

  

    def __init__(self, *args, **kwargs):
        super(ResgisterUserForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'

class GuestUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class OwnerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }


class UserFormG(forms.ModelForm):
    class Meta:
        model=GuestUser
        fields=['gender',]


class UserFormS(forms.ModelForm):
    class Meta:
        model=StoreOwner
        fields=['gender',]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [ 'first_name','last_name','username', 'email','password']

# Create a ProfileUpdateForm to update gender
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model =GuestUser
        fields = ['gender',]