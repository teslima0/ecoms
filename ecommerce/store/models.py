from asyncio.windows_events import NULL
from itertools import product

from unicodedata import digit, name
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import migrations


from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'customer', null=True, blank=True)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)

    def __str__(self) :
        return self.name

  

class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    digital=models.BooleanField(default=False, null=True, blank=False)
    description=models.CharField(max_length=200,null=True)
    image=models.ImageField(upload_to='store/product/',null=True,blank=True)

    def __str__(self) :
        return self.name

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url

class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name = 'customer', null=True, blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False, null=True,blank=False)
    transaction_id=models.CharField(max_length=200, null=True)

    
    #def __str__(self):
        #if str(self.customer.name) or '-':
            #return str(self.customer.name)
        #elif self.customer==None:
           ## return ''
        #else:
            #return str(self.customer.email)
    def __str__(self) :
      
        return str(self.id) 
    
   #get email
    @property
    def get_email(self):
        customers=self.customer.email
        
        return customers

    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    

    @property
    def get_total(self):
        total=self.product.price *self.quantity
        return total

class Shipping(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=200,null=True, default='')
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.address


"""
# method for updating
@receiver(post_save, sender=User)
def update_customer(sender, instance,  **kwargs):
    instance.order.customer.name = 'abc'
    instance.order.customer.email = 'abv@gmail.com'
    instance.order.save()
    
    Order.objects.create(customer=instance)
"""