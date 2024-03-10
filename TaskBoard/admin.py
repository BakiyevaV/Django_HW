from django.contrib import admin
from .models import Tasks, Subscribes, Vendors, Vendors_Icecream, LimitedEditionIcecream

# Register your models here.
admin.site.register(LimitedEditionIcecream)
admin.site.register(Vendors)
admin.site.register(Vendors_Icecream)