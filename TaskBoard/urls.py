from django.contrib import admin
from django.urls import path

from TaskBoard.views import create_task, get_all_tasks, about_task, delete_task, save_subscribes

app_name = 'taskboard'

urlpatterns = [
    path('', get_all_tasks, name='all_tasks'),
    path('create_task/', create_task, name='create_task'),
    path('about_task/<int:task_id>/', about_task, name='about_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('subscribe/', save_subscribes, name='subscribe')

]