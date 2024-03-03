from django.contrib import admin
from .models import Tasks, Subscribes, Icecream, Vendors, Vendors_Icecream, Clients, AdvUser

# Register your models here.
admin.site.register(Icecream)
admin.site.register(Vendors)
admin.site.register(Vendors_Icecream)