from django.contrib.auth import authenticate
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.paginator import Paginator
from django.db.transaction import atomic

from .models import Tasks, Subscribes, Icecream, LimitedEditionIcecream
from .forms import TaskForm, StatusForm, IcecreamForm, TaskEditFormset
from django.views.decorators.http import require_http_methods
from django.db import transaction

from django.shortcuts import render, redirect
from django.urls import reverse
import datetime


# Create your views here

@require_http_methods(['GET', 'POST'])
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('taskboard:all_tasks')
    else:
        form = TaskForm()
    tasks = Tasks.actions.all()
    total_tasks_count = tasks.count()
    not_started_tasks_count = Tasks.actions.not_started_count()
    done_tasks_count = Tasks.actions.done_count()
    in_process_tasks_count = Tasks.actions.in_progress_count()

    context = {'form': form, 'tasks': tasks, 'total_tasks_count': total_tasks_count,
                'not_started_tasks_count': not_started_tasks_count,
                'done_tasks_count': done_tasks_count, 'in_process_tasks_count': in_process_tasks_count,
                'active_page': 'create task', 'title': 'Create new task'}
    return render(request, 'new_task.html', context)

    # if request.method == 'POST':
    #     implementer = request.POST.get('implementer')
    #     author = request.POST.get('author')
    #     title = request.POST.get('title')
    #     deadline = request.POST.get('deadline')
    #     description = request.POST.get('description')
    #     print(description)
    #     task = Tasks(implementer=implementer, author=author, title=title,
    #                  deadline=deadline, description=description)
    #
    #     task.save()
    #     return redirect('taskboard:all_tasks')
    #
    # tasks = Tasks.objects.all()
    # total_tasks_count = tasks.count()
    # not_started_tasks_count = tasks.filter(status="n").count()
    # done_tasks_count = tasks.filter(status="d").count()
    # in_process_tasks_count = tasks.filter(status="p").count()
    # context = {'tasks': tasks, 'total_tasks_count': total_tasks_count,
    #                'not_started_tasks_count': not_started_tasks_count,
    #                'done_tasks_count': done_tasks_count, 'in_process_tasks_count': in_process_tasks_count,
    #            'active_page': 'create task', 'title': 'Create new task'}
    # return render(request, 'new_task.html', context)


def get_all_tasks(request):
    model = Tasks
    tasks = model.actions.order_by_title_length()
    total_tasks_count = tasks.count()
    not_started_tasks_count = Tasks.actions.not_started_count()
    done_tasks_count = Tasks.actions.done_count()
    in_process_tasks_count = Tasks.actions.in_progress_count()
    paginator = Paginator(tasks, per_page=2, orphans=0)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'tasks': page.object_list, 'page_obj': page, 'total_tasks_count': total_tasks_count,
               'not_started_tasks_count': not_started_tasks_count, 'done_tasks_count': done_tasks_count,
               'in_process_tasks_count': in_process_tasks_count, 'active_page': 'all tasks', 'title': 'All tasks'}
    return render(request, 'index.html', context)


@require_http_methods(['GET', 'POST'])
def about_task(request, task_id):
    model = Tasks
    task = model.actions.get(pk=task_id)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=task)
        if form.is_valid():
            status = form.cleaned_data['status']
            print("статус",status)
            model.actions.all().filter(pk=task_id).update(status=status)
            if status == 'd':
                model.actions.all().filter(pk=task_id).update(done_date=datetime.datetime.now())
            else:
                if model.actions.get(pk=task_id).done_date != None:
                    row = model.actions.get(pk=task_id)
                    row.done_date = None
                    row.save()
            return redirect(reverse('taskboard:about_task', args=[task_id]))
    else:
        form = StatusForm(instance=task)
    context = {'task': task, 'form': form , 'title': 'About task'}
    return render(request, 'product-details.html', context)

def delete_task(request, task_id):
    Tasks.actions.filter(pk=task_id).delete()
    return redirect(reverse('taskboard:all_tasks'))
@require_http_methods(['POST'])
def save_subscribes(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subscribe = Subscribes(email=email)
        subscribe.save()
        return redirect('taskboard:all_tasks')


def create_icecream(request):
    special_fields = ['theme', 'season', 'sale_start_date', 'sale_end_date', 'unique_flavors']
    if request.method == 'POST':
        icecream_form = IcecreamForm(request.POST)
        if icecream_form.is_valid():
            icecream_form.save()
            return redirect('taskboard:icecream')
        else:
            icecream_form = IcecreamForm(request.POST)
            print('не проходит')
            context = {'message':'Введены некорректные данные', 'title': 'Create icecream',
                       'icecream_form': icecream_form, 'active_page': 'create icecream',
                       'special_fields': special_fields}
            return render(request, 'create_icecream.html', context)

    else:
        icecream_form = IcecreamForm()
    context = {'icecream_form': icecream_form, 'active_page': 'create icecream',
                   'title': 'Create icecream', 'special_fields': special_fields}
    return render(request, 'create_icecream.html', context)

def get_icecream(request):
    icecream = LimitedEditionIcecream.objects.all()
    paginator = Paginator(icecream, per_page=2, orphans=0)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'icecream': icecream, 'page_obj': page, 'active_page': 'icecream', 'title': 'Icecream'}
    return render(request, 'index.html', context)

def edit_task(request):
    model = Tasks
    if request.method == 'POST':
        formset = TaskEditFormset(request.POST,  queryset=model.actions.all())
        for form in formset.forms:
            if form.instance.deadline:
                form.initial['deadline'] = form.instance.deadline.strftime('%Y-%m-%d')
            if form.instance.done_date:
                form.initial['done_date'] = form.instance.done_date.strftime('%Y-%m-%d')
        if formset.is_valid():
            for form in formset:
                try:
                    form.save()
                    transaction.on_commit(commit_handler)
                    context = {'message': 'Изменения приняты', 'formset': formset, 'title': 'Edit task',
                               'active_page': 'Edit task'}
                    return render(request, 'edit_task.html', context)
                except:
                    transaction.rollback()
                    context = {'message': 'Что-то пошло не так', 'formset': formset, 'title': 'Edit task',
                               'active_page': 'Edit task'}
                    return render(request, 'edit_task.html', context)
        else:
            context = {'message': 'Введены некорректные данные', 'formset': formset, 'title': 'Edit task',
                       'active_page': 'Edit task'}
            transaction.commit()
            return render(request, 'edit_task.html', context)
    else:
        formset = TaskEditFormset(queryset=model.actions.all())
        for form in formset.forms:
            if form.instance.deadline:
                form.initial['deadline'] = form.instance.deadline.strftime('%Y-%m-%d')
            if form.instance.done_date:
                form.initial['done_date'] = form.instance.done_date.strftime('%Y-%m-%d')
        context = {'formset': formset, 'title': 'Edit task', 'active_page': 'Edit task'}
        return render(request, 'edit_task.html', context)


def commit_handler():
    print('Транзакция прошла успешно!')



















