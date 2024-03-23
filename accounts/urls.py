from django.urls import path, re_path
from django.contrib.auth.views import LoginView

from .views import UserCreateView, AllUsersView, UserDetailView, UsersByPeriodView, UserLoginView

app_name = 'accounts'
urlpatterns = [
    re_path(r'^r\w{2}/$', UserCreateView.as_view(), name='registration'),
    re_path(r'^l\w*/$', UserLoginView.as_view(), name='login'),
    path('users/', AllUsersView.as_view(), name='users'),
    path('get_period/<int:year>/<int:month>/', UsersByPeriodView.as_view(), name='period'),
    path('userdetail/<int:user_id>/', UserDetailView.as_view(), name='user_detail')
]


