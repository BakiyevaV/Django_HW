from django.contrib import admin
from django.urls import path
from home_work_09Nov.views import index, object_passport

urlpatterns = [
    path('', index),
    path('object_passport/<int:param>/', object_passport),
    path('admin/', admin.site.urls),
]
