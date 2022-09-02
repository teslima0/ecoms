from ast import Pass
import imp
import json
from .forms import ProductForm,CategoryForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from . utils import cookieCart, cartData, guestOrder
from pypaystack import Transaction, Customer, Plan
from django.conf import settings
#from account.views import is_customer

from django.contrib import auth
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings

@login_required(login_url='account:loginpage')
def productDetail(request, pk):
	data=cartData(request)
	
	cartItems=data['cartItems']
	products = Product.objects.get(id=pk)
	
	context = {
        'products': products,
		'cartItems':cartItems 
       
   	 }
	
	return render(request, 'store/productDetail.html', context)



def searchBar(request):
	data=cartData(request)
	cartItems=data['cartItems']
	
		
	query = request.POST['query']
	if query:
		products = Product.objects.filter(name__contains=query) 
			
		context = {
            "products":products,
			"cartItems":cartItems
   			 }
            
		return render(request, 'store/searchbar.html', context)
            #return redirect('store',context)
	else:
		print("No information to show")
		return render(request, 'store/searchbar.html', {})

@login_required(login_url='account:loginpage')
def shippingView(request):
	data=cartData(request)
	cartItems=data['cartItems']
	shippings= Shipping.objects.all()
	#print(shippings)
	messages.success(request,("New Shipping Information"))
	return render(request,'store/shipping_info.html',{'shippings':shippings, 'cartItems':cartItems})

@login_required(login_url='account:loginpage')
def OrderView(request):
	data=cartData(request)
	cartItems=data['cartItems']

	ordering=[]
	tab=[]
	orderitems= OrderItem.objects.all()
	for orderitem in orderitems:
		orders= Order.objects.filter(orderitem=orderitem)
		ordering.append(orders)
		for order in orders:
			print(order.transaction_id)
		tab.append(order)
	#print(tab)
	#print(ordering[0][0])
	messages.success(request,("New order added"))
	return render(request, 'store/orderView.html',{"orders":tab, 'cartItems':cartItems})

@login_required(login_url='account:loginpage')
def OrderItemView(request):
	data=cartData(request)
	cartItems=data['cartItems']

	orderitems= OrderItem.objects.all()
	print(orderitems)
	messages.success(request,("New order details"))
	return render(request, 'store/orderItemView.html',{"orderitems":orderitems,'cartItems':cartItems})

@login_required(login_url='account:loginpage')
def addCategory(request):
	data=cartData(request)
	cartItems=data['cartItems']
	form = CategoryForm()

	if request.method == 'POST':
		if request.user.is_superuser:
			form = CategoryForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request,("New product category added"))
				return redirect('store')
	else:
		if request.user.is_superuser:
			form = CategoryForm()

	context = {
		"form":form,
		"cartItems":cartItems
	}

	return render(request, 'store/addcategory.html', context)

@login_required(login_url='account:loginpage')
def CategoryView(request):
	data=cartData(request)
	cartItems=data['cartItems']

	categories= Category.objects.all()
	print(categories)
	return render(request, 'store/CategoryView.html',{"categories":categories,'cartItems':cartItems})

@login_required(login_url='account:loginpage')
def updateCategory(request,pk):
	data=cartData(request)
	cartItems=data['cartItems']
	category = Category.objects.get(id=pk)

	form = CategoryForm(instance=category)

	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			form.save()
			messages.success(request,("Product category updated"))
			return redirect('ViewCategory')

	context = {
        "form":form,
		"cartItems":cartItems
    }

	return render(request, 'store/updateCategory.html', context)

@login_required(login_url='account:loginpage')
def deleteCategory(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    messages.success(request,('Product Category deleted'))
    return redirect('ViewCategory')

@login_required(login_url='account:loginpage')
def addProduct(request):
	data=cartData(request)
	cartItems=data['cartItems']
	form = ProductForm()

	if request.method == 'POST':
		if request.user.is_superuser:
			form = ProductForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				messages.success(request,("New product added"))
				return redirect('store')
	else:
		if request.user.is_superuser:
			form = ProductForm()

	context = {
		"form":form,
		"cartItems":cartItems
	}

	return render(request, 'store/addProduct.html', context)

@login_required(login_url='account:loginpage')
def updateProduct(request,pk):
	data=cartData(request)
	cartItems=data['cartItems']
	product = Product.objects.get(id=pk)

	form = ProductForm(instance=product)

	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES, instance=product)
		if form.is_valid():
			form.save()
			messages.success(request,("Product updated"))
			return redirect('store')

	context = {
        "form":form,
		"cartItems":cartItems
    }

	return render(request, 'store/updateProduct.html', context)

@login_required(login_url='account:loginpage')
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    messages.success(request,("Product deleted"))
    return redirect('store')

def store(request):
	
	data=cartData(request)
	cartItems=data['cartItems']

	category = request.GET.get('category')
	
	p=Paginator(Product.objects.all(), 6)
	page=request.GET.get('page')
	listproduct=p.get_page(page)
	nums= 'a' * listproduct.paginator.num_pages
	if category == None:
		
		#p=Paginator(Product.objects.all(), 6)
		#page=request.GET.get('page')
		listproduct=p.get_page(page)
		#nums= 'a' * listproduct.paginator.num_pages
	else:
		listproduct = Product.objects.filter(category__name=category).order_by("-price")
	
	categories = Category.objects.all()
	context = {'categories':categories, 'cartItems':cartItems,'nums':nums, 'listproduct':listproduct}
	
	
	return render(request, 'store/store.html', context)

class  CustomerProfileView(TemplateView):
      template_name = "store/CustomerProfile.html"


     

      def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context


def cart(request):

	
	data=cartData(request)
	cartItems=data['cartItems']
	order=data['order']
	items=data['items']	
	
	context = {'items':items,'order':order,'cartItems':cartItems}
	
	return render(request, 'store/cart.html', context)


def checkout(request):
	pk_public=settings.PAYSTACK_PUBLIC_KEY
	#Create empty cart for now for non-logged in user
	if request.user.is_authenticated:
		data=cartData(request)
		customer_email=data['customer']
		for email in customer_email:
				Pass
		try:
			email=email
		except:
			email=''
		#print(email)
		cartItems=data['cartItems']
		order=data['order']
		items=data['items']
        
		context = {'cartItems':cartItems, 'order':order, 'items':items,'customer_email':email,'pk_public':pk_public}
		return render(request, 'store/checkout.html', context)

	else:
		return redirect('account:loginpage')
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)


#@csrf_exempt
def processOrder(request):
	#print('Data:', request.body)
	transaction_id=datetime.datetime.now().timestamp()
	print(transaction_id)
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer=request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		
		

	else:
		customer, order = guestOrder(request, data)
		print('user is not logged in..')

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		Shipping.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)

	return JsonResponse('payment completed', safe=False)


