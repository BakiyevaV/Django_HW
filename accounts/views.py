import json
import datetime
import calendar

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpHeaders
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ArchiveIndexView, MonthArchiveView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, ListView

from bboard.models import Rubric, Bb
from .models import Clients
from .forms import UserForm, MyLoginForm, changePasswordForm
from django.shortcuts import redirect
from django.core.mail import EmailMessage, get_connection


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

def reset_pass(request):
    staff = User.objects.filter(is_staff=True)
    messages = []
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user is not None:
                user.set_password(email)
                user.save()
                context = {'user': user.username, 'pk': user.pk }
                letter = render_to_string('email/letter.html', context)
                user_email = EmailMessage(
                    subject='Оповещение',
                    body=letter,
                    to=[user.email]
                )
                user_email.content_subtype = 'html'  # Устанавливаем тип содержимого письма
                messages.append(user_email)

                for employee in staff:
                    messages.append(EmailMessage(
                        subject='Оповещение',
                        body=f'Пользователь {user.username} забыл пароль',
                        to=[employee.email]
                    ))
                connection = get_connection()
                connection.open()
                connection.send_messages(messages)
                connection.close()

                return redirect(reverse('accounts:login'))
            else:
                context = {'error_message': 'Пользователь с указанным email не найден!'}
                return render(request, 'reset_pass.html', context)
        else:
            context = {'error_message': 'Введите email!'}
            return render(request, 'reset_pass.html', context)
    return render(request, 'reset_pass.html')

def new_pass(request, pk):
    template_name = 'change_password.html'
    user = User.objects.filter(pk=pk).first()
    if user is None:
        return render(request, 'some_error_template.html', {'error_message': 'Пользователь не найден.'})

    if request.method == 'POST':
        form = changePasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get("password")
            password2 = form.cleaned_data.get("confirm_password")
            if password1 == password2:
                user.set_password(password1)
                user.save()
                print(user.username)
                user = authenticate(request, username=user.username, password=password1)
                if user is None:
                    print('Не удалось авторизовать пользователя после смены пароля.')
                else:
                    print(f'Пользователь {user.username} успешно авторизован!')
                    login(request, user)
                    return redirect('bboard:index')
            else:

                context = {'error_message': 'Пароли должны быть одинаковыми', 'form': form}
                return render(request, template_name, context)
        else:

            context = {'error_message': 'Пароль не соответствует политике безопасности', 'form': form}
            return render(request, template_name, context)

    form = changePasswordForm()
    context = {'form': form}
    return render(request, template_name, context)





















