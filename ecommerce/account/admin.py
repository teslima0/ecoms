from django.contrib import admin
from . models import GuestUser,StoreOwner
# Register your models here.

admin.site.register(GuestUser)
admin.site.register(StoreOwner)