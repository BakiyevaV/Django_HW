
from django.core import validators
from django.forms import ModelForm, modelform_factory, Form, modelformset_factory, BaseModelFormSet
from .models import Tasks, Icecream, SpecialIcecream, LimitedEditionIcecream
from django.forms.widgets import DateInput, Select
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from datetime import date
from django import forms

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
    is_limited = forms.BooleanField(label="Ограниченная серия")
    class Meta:
        model = LimitedEditionIcecream
        fields = ('name', 'fabricator', 'composition', 'price', 'package', 'weight', 'expiration_date_in_days',
                  'vegan', 'sugar_free', 'is_limited', 'theme', 'season', 'sale_start_date', 'sale_end_date',
                  'unique_flavors')
        widgets = {'package': Select(attrs={'size': 3}),
                   'sale_start_date': forms.SelectDateWidget(attrs={'class': 'date-select-class'}),
                   'sale_end_date': forms.SelectDateWidget(attrs={'class': 'date-select-class'})
                   }
    
    def __init__(self, *args, **kwargs):
        super(IcecreamForm, self).__init__(*args, **kwargs)
        self.fields['price'].validators.append(validate_price)
        self.fields['weight'].validators.append(validate_weight)


class CaptchaTestForm(Form):
    captcha = CaptchaField()


# class UserForm(ModelForm):
#     class Meta:
#         model = AdvUser
#         fields = ('username', 'password', 'email', 'birth_date', 'is_activated', 'is_staff', 'is_superuser')
#
#         widgets = {
#             'password': forms.PasswordInput(),
#             'birth_date': forms.SelectDateWidget(attrs={'class': 'date-select-class'})
#         }
