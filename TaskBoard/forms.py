from django.forms import ModelForm, modelform_factory, Form
from .models import Tasks, Icecream
from django.forms.widgets import DateInput, Select
from captcha.fields import CaptchaField

TaskForm = modelform_factory(model=Tasks, exclude=('status', 'done_date'),
                             labels={'title': 'Название задачи'},
                             widgets={'deadline': DateInput(attrs={'type': 'date'})})

class StatusForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ('status',)


IcecreamForm = modelform_factory(model=Icecream, fields='__all__',
                                 widgets={'package': Select(attrs={'size': 3})})

class CaptchaTestForm(Form):
    captcha = CaptchaField()

