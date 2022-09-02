from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from .models import StoreOwner,GuestUser
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from .forms import OwnerUserForm,GuestUserForm, ResgisterUserForm,UserFormG,UserFormS,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from store.models import Customer
from store.utils import cookieCart, cartData, guestOrder
def logout_user(request):
    logout(request)
    messages.success(request,("You have logged out"))
    return redirect ('store')

def store_signup_view(request):
    userForm=OwnerUserForm()
    userForms=UserFormS()
    mydict={'userForm':userForm,
            'userForms':userForms
    
    }
    if request.method=='POST':
        userForm=OwnerUserForm(request.POST)
        userForms=UserFormS(request.POST)
   
        if userForm.is_valid() and userForms.is_valid() :
            user=userForm.save()
            #user.set_password(user.password)
            user.save()
            user.set_password(user.password)
            user.save()
            storeowner=userForms.save(commit=False)
            storeowner.user=user
            storeowner.save()
            Customer.objects.create(
                    user = user,
                    name = user.username,
                    email = user.email
                )    
            #username= guest.cleaned_data.get('username') 
            
            my_customer_group = Group.objects.get_or_create(name='ADMIN')
            my_customer_group[0].user_set.add(user)
            messages.success(request, f'Your Account has been created! You can now log in')
            redirect('account:loginpage')
    return render(request,'storesignup.html',context=mydict)


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

def is_adminstore(user):
    return user.groups.filter(name='ADMIN').exists()

def guest_signup_view(request):
    data=cartData(request)
    cartItems=data['cartItems']
    guestuserForm=GuestUserForm(request.POST)
    userFormg=UserFormG(request.POST)
   
    if request.method=='POST':
        guestuserForm=GuestUserForm(request.POST)
        userFormg=UserFormG(request.POST)
        if guestuserForm.is_valid() and userFormg.is_valid() :
            user=guestuserForm.save()
            user.save()
            user.set_password(user.password)
            user.save()
            guest=userFormg.save(commit=False)
            guest.user=user
            guest.save()
            Customer.objects.create(
                    user = user,
                    name = user.username,
                    email = user.email
                )    
            #username= guest.cleaned_data.get('username') 
            
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            messages.success(request, f'Your Account has been created! You can now log in')
            return redirect('account:loginpage')
    mydict={'guestuserForm':guestuserForm,'userformg':userFormg,"cartItems":cartItems}     
    return render(request,'guest.html',context=mydict)

@login_required(login_url='account:loginpage')
def profileUdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'updateProfile.html', context)
"""
def register(request):
        if request.method == 'POST':
            form = ResgisterUserForm(request.POST)
            if form.is_valid(): 
                #saving the registered user
                user = form.save()
                Customer.objects.create(
                    user = user,
                    name = user.username,
                    email = user.email
                )    
                username= form.cleaned_data.get('username') 
                messages.success(request, f'Your Account has been created! You can now log in')
                return redirect('account:loginpage')
        else:
            form = ResgisterUserForm() #creates an empty form
        return render(request, 'register.html', {'form': form})

"""
def login_user(request):
    data=cartData(request)
    cartItems=data['cartItems']
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("Congrat! you logged in successfully!"))
            return redirect ('store')

        else:
            messages.success(request,("Wrong username or password, try again..."))
            return redirect ('account:loginpage')


    else:

        return render(request, 'login.html', {"cartItems":cartItems})