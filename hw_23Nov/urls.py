from django.contrib import admin
from django.urls import path,include
from .views import index, get_child

urlpatterns = [
    path('', index),
    path('get_child/<str:param>/', get_child, name='get_child'),
]