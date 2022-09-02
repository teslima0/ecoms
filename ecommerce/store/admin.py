from django.contrib import admin

from .models import Product,Shipping,Order,OrderItem,Customer,Category
# Register your models here.

admin.site.register( Product)
admin.site.register(Shipping)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Category)
