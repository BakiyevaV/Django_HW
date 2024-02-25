from django.core import validators
from django.forms import ModelForm, modelform_factory, Form, modelformset_factory, BaseModelFormSet
from .models import Tasks, Icecream
from django.forms.widgets import DateInput, Select
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from datetime import date

def validate_price(val):
    if val <= 0:
        raise ValidationError('Стоимость не корректна')
    
def validate_weight(val):
     if val <= 20:
        raise ValidationError('Недопустимо малый вес')

TaskForm = modelform_factory(model=Tasks, exclude=('status', 'done_date'),
                             labels={'title': 'Название задачи'},
                             widgets={'deadline': DateInput(attrs={'type': 'date'})})

class StatusForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ('status',)

class TaskFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            print(form.cleaned_data)
            if form.cleaned_data:
                if form.cleaned_data['title']:
                    title = form.cleaned_data['title']
                    print('t'+title)
                    if len(title) < 4:
                        raise ValidationError('Слишком короткое наименование задачи')
                if form.cleaned_data['done_date']:
                    done_date = form.cleaned_data['done_date'].date()
                    if done_date > date.today():
                        raise ValidationError('Такая дата еще не наступила')



TaskEditFormset = modelformset_factory(model=Tasks, formset=TaskFormSet, fields='__all__', extra=1, can_delete=True,
                                       widgets={'deadline': DateInput(attrs={'type': 'date'}),
                                                'done_date': DateInput(attrs={'type': 'date'})})

class IcecreamForm(ModelForm):
    class Meta:
        model = Icecream
        fields = '__all__'
        widgets = {'package': Select(attrs={'size': 3})}
    
    def __init__(self, *args, **kwargs):
        super(IcecreamForm, self).__init__(*args, **kwargs)
        self.fields['price'].validators.append(validate_price)
        self.fields['weight'].validators.append(validate_weight)


class CaptchaTestForm(Form):
    captcha = CaptchaField()

