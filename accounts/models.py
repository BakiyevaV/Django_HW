from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator, CommonPasswordValidator
from django.contrib.auth.models import User

class PassValidator():
    def __init__(self,password):
        self.password=password
    def check_item(self):
        upper_count = 0
        lower_count = 0
        digit_count = 0
        spec_signs_count = 0
        signs = ["!", "@", "#", "$", "%", "^", "&", "*", "-", "+", "/"]
        for letter in self.password:
            if letter.isupper():
                upper_count += 1
            elif letter.islower():
                lower_count += 1
            elif letter.isdigit():
                digit_count += 1
            elif letter in signs:
                spec_signs_count += 1
        if upper_count > 0 and lower_count > 0 and digit_count > 0 and spec_signs_count > 0:
            return True

    def __call__(self,value):
        if len(value) < 6 or not self.check_item():
            raise ValidationError('Пароль должен содержать не менее 6 символов и не менее одной прописной буквы, строчной буквы, цифры и специального знака',
                                  code='out_of_range', params={'password':value})


class Clients(models.Model):
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30, unique=True, validators = [PassValidator])
    email = models.CharField(max_length=30, unique=True, validators=[validators.RegexValidator(regex='\w[\w\.-]*\w+@\w[\w\.]*\.[a-zA-Z]{2,3}')], error_messages= {'invalid':'Введите корректный адрес электронной почты'})
    birth_date = models.DateField()
    is_blocked = models.BooleanField(default=False)

    class Meta:
        # доп настройки модели
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['pk'] #можно несколько параметров


# Create your models here.


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Spare(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)

    def __str__(self):
        return self.name
