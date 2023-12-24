from django.urls import path

from .views import UserCreateView,login_view

urlpatterns = [
    path('reg/', UserCreateView.as_view(), name='registration'),
    path('login/', login_view, name='login'),
]


