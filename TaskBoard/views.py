from .models import Tasks
from .forms import TaskForm, StatusForm
from django.views.decorators.http import require_http_methods

from django.shortcuts import render, redirect
from django.urls import reverse
import datetime


# Create your views here

@require_http_methods(['GET', 'POST'])
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('taskboard:all_tasks')
    else:
        form = TaskForm()
    return render(request, 'new_task.html', {'form': form})

def get_all_tasks(request):
    model = Tasks
    tasks = model.objects.all()
    context = {'tasks': tasks}
    return render(request, 'all_tasks.html', context)


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
            return redirect(reverse('taskboard:about_task', args=[task_id]))
    else:
        form = StatusForm(instance=task)
    context = {'task': task, 'form': form}
    return render(request, 'task.html', context)

def delete_task(request, task_id):
    Tasks.objects.filter(pk=task_id).delete()
    return redirect(reverse('taskboard:all_tasks'))



