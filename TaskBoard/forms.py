from django.forms import ModelForm
from .models import Tasks

class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ('implementer', 'author', 'title', 'description', 'deadline')

class StatusForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ('status',)
