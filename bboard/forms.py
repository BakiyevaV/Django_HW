from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet
from django.core import validators
from django import forms
from .models import Bb, Comments, Rubric


# class BbForm(BaseInlineFormSet):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric', 'feature')


class BbForm(ModelForm):
    title = forms.CharField(
        label='Название товара',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Слишком короткое название товара'})
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'feature')

    def clean_title(self):
        val = self.cleaned_data.get('title')
        if val == 'Прошлогодний снег':
            print('к продаже не допускается')
            raise ValidationError('к продаже не допускается')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data.get('content'):
            errors['content'] = ValidationError('Нет описания')
        if errors:
            raise ValidationError(errors)
class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('comment_creator', 'comment')
class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово', required=True)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')

    captcha = CaptchaField(
        label='Введите текст с картинки',
        error_messages={'invalid':'Неправильный текст'},
        generator='captcha.helpers.math_challenge',
    )

    error_css_class = 'error'
