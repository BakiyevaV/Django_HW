import json
import datetime
import calendar

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpHeaders
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ArchiveIndexView, MonthArchiveView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, ListView

from .models import Clients
from .forms import UserForm, MyLoginForm
from django.shortcuts import redirect


class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserForm
    model = User
    success_url = "index.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect(reverse('bboard:index'))

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = MyLoginForm

#
# def login_view(request):
#     if request.method == 'POST':
#         request_write(request)
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['login']
#             password = form.cleaned_data['password']
#             user = None
#             users = Clients.objects.all()
#             users_admin = User.objects.all()
#             for u in users_admin:
#                 if u.username == username:
#                     user = u
#             if user is not None:
#                 return redirect(reverse('bboard:index'))
#             else:
#                 context = {'form': form, 'error_message': 'Неверные учетные данные. Пожалуйста, проверьте логин и пароль.'}
#                 return render(request, 'login.html', context)
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

def request_write(request):
    data = {}
    request_params = ('scheme', 'body', 'path', 'method', 'encoding', 'content_type', 'GET',
                      'POST', 'COOKIES', 'FILES', 'headers',
                      {'META': ('CONTENT_LENGTH', 'CONTENT_TYPE', 'HTTP_ACCEPT', 'HTTP_HOST', 'HTTP_REFERER',
                                'HTTP_USER_AGENT', 'QUERY_STRING', 'REMOTE_ADDR')})
    with open('logs.json', 'w', encoding='utf-8') as log_file:
        print(request.META["HTTP_HOST"])
        for param in request_params:
            if type(param) == str:
                data[param] = decoder(getattr(request, param))
            else:
                m_key = ""
                meta_p = {}
                for key, subparams in param.items():
                    m_key = key
                    obj = getattr(request, key)
                    for subparam in subparams:
                        meta_p[f'{subparam}'] = decoder(obj[f'{subparam}'])

                data[m_key] = meta_p
        data_for_write = {f"{datetime.datetime.now()}":data}
        json.dump(data_for_write, log_file)

def decoder(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    elif isinstance(value, HttpHeaders):
        return dict(value)
    return value

class AllUsersView(ArchiveIndexView):
    model = Clients
    template_name = 'users.html'
    date_field = 'birth_date'
    date_list_period = 'month'
    context_object_name = 'users'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        updated_date_list = []
        for date in context['date_list']:
            month_name = calendar.month_name[date.month]
            updated_date_list.append({
                'year': date.year,
                'month': month_name,
                'day': date.day
            })

        context['date_list'] = updated_date_list
        return context

class UsersByPeriodView(MonthArchiveView):
    model = Clients
    template_name = 'users.html'
    date_field = 'birth_date'
    date_list_period = 'month'
    month_format = '%m'
    context_object_name = 'users'
    allow_empty = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        updated_date_list = []
        for date in context['date_list']:
            month_name = calendar.month_name[date.month]
            updated_date_list.append({
                'year': date.year,
                'month': month_name,
                'day': date.day
            })

        context['date_list'] = updated_date_list
        return context

class UserDetailView(DetailView):
    model = Clients
    template_name = 'userdetail.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'
    def get_object(self, queryset=None):
        return Clients.objects.get(id=self.kwargs['user_id'])

# from django.contrib.auth.models import User
# admin = User.objects.get(name='admin')
# if admin.check_password('password'):
#     # дальнейшие действия при совпадении
#     pass
# else:
#     # дальнейшие действия при несовпадении
#     pass

# admin.set_password('newpassword')
# admin.save()




















