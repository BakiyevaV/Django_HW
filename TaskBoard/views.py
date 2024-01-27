from .models import Tasks, Subscribes
from .forms import TaskForm, StatusForm
from django.views.decorators.http import require_http_methods

from django.shortcuts import render, redirect
from django.urls import reverse
import datetime


# Create your views here

@require_http_methods(['GET', 'POST'])
def create_task(request):
    if request.method == 'POST':
        implementer = request.POST.get('implementer')
        author = request.POST.get('author')
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        task = Tasks(implementer=implementer, author=author, title=title,
                     deadline=deadline, description=description)

        task.save()
        return redirect('taskboard:all_tasks')

    tasks = Tasks.objects.all()
    total_tasks_count = tasks.count()
    not_started_tasks_count = tasks.filter(status="n").count()
    done_tasks_count = tasks.filter(status="d").count()
    in_process_tasks_count = tasks.filter(status="p").count()
    context = {'tasks': tasks, 'total_tasks_count': total_tasks_count,
                   'not_started_tasks_count': not_started_tasks_count,
                   'done_tasks_count': done_tasks_count, 'in_process_tasks_count': in_process_tasks_count}
    return render(request, 'new_task.html',context)

def get_all_tasks(request):
    model = Tasks
    tasks = model.objects.all()
    total_tasks_count = tasks.count()
    not_started_tasks_count = tasks.filter(status="n").count()
    done_tasks_count = tasks.filter(status="d").count()
    in_process_tasks_count = tasks.filter(status="p").count()
    context = {'tasks': tasks, 'total_tasks_count': total_tasks_count, 'not_started_tasks_count':not_started_tasks_count,
               'done_tasks_count': done_tasks_count,  'in_process_tasks_count': in_process_tasks_count}
    return render(request, 'index.html', context)


@require_http_methods(['GET', 'POST'])
def about_task(request, task_id):
    model = Tasks
    task = model.objects.get(pk=task_id)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=task)
        if form.is_valid():
            status = form.cleaned_data['status']
            print("статус",status)
            model.objects.all().filter(pk=task_id).update(status=status)
            if status == 'd':
                model.objects.all().filter(pk=task_id).update(done_date=datetime.datetime.now())
            else:
                if model.objects.get(pk=task_id).done_date != None:
                    row = model.objects.get(pk=task_id)
                    row.done_date = None
                    row.save()
            return redirect(reverse('taskboard:about_task', args=[task_id]))
    else:
        form = StatusForm(instance=task)
    context = {'task': task, 'form': form}
    return render(request, 'product-details.html', context)

def delete_task(request, task_id):
    Tasks.objects.filter(pk=task_id).delete()
    return redirect(reverse('taskboard:all_tasks'))
@require_http_methods(['POST'])
def save_subscribes(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subscribe = Subscribes(email=email)
        subscribe.save()
        return redirect('taskboard:all_tasks')





