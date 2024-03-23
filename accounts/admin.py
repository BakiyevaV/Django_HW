from django.contrib import admin
from .models import AdvUser

# Register your models here.
# class AdvUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'password')


admin.site.register(AdvUser)