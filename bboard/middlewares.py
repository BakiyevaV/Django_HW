from django.contrib.auth.models import User
from django.db.models import Count

from bboard.models import Rubric


def my_middleware(_next):
    #инициализация
    def core_middleware(request):
        #обработка клиентского запроса
        response = _next(request)
        print('РАБОТАЕТ')
        # обработка ответа
        return response
    return core_middleware


class MyMiddleware:
    def __init__(self, get_response):
        self._next = get_response

    def __call__(self, request):
        # обработка клиентского запроса
        response = self._next(request)
        print('РАБОТАЕТ')
        # обработка ответа
        return response


class RubricMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_template_response(self, request, response):
        response.context_data['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return response


def rubrics(request):
    return {'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}

class UserMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)
    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            username = request.user.username
            user = User.objects.get(username=username)
            user_groups = user.groups.all()
            response.context_data['username'] = user
            response.context_data['user_groups'] = user_groups
        else:
            response.context_data['username'] = 'Гость'
        print(user, user_groups)
        return response

def user_context_proc(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        user_groups = user.groups.all()
        return {'username': username, 'user_groups': user_groups}
    else:
        username = 'Гость'
        return {'username': username}


