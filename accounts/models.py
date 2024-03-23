from django.contrib.postgres.fields import DateTimeRangeField, ArrayField, HStoreField, CICharField
from django.contrib.postgres.indexes import GistIndex
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator, CommonPasswordValidator
from django.contrib.auth.models import User
from django.db.models import JSONField

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
    password = models.CharField(max_length=30, unique=True, validators=[PassValidator])
    email = models.CharField(max_length=30, unique=True, validators=[validators.RegexValidator(regex='\w[\w\.-]*\w+@\w[\w\.]*\.[a-zA-Z]{2,3}')], error_messages= {'invalid':'Введите корректный адрес электронной почты'})
    birth_date = models.DateField()
    is_blocked = models.BooleanField(default=False)

    class Meta:
        # доп настройки модели
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'#можно несколько параметров


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
    spares = models.ManyToManyField(Spare, through='Kit', through_fields=('machine', 'spare'))

    def __str__(self):
        return self.name

class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

# class PGSRoomReserving(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Помещение')
#     reserving = DateTimeRangeField(verbose_name='Время резервирования')
#     cancelled = models.BooleanField(default=False, verbose_name='Отменить резервирования')
#     class Meta:
#         indexes = [
#             GistIndex(fields=['reserving'], name='i_pgsrr_reserving',
#                       opclasses=('range_ops',),
#                       fillfactor=50)
#         ]
#
# class PGSRubric(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Имя')
#     description = models.TextField(verbose_name='Описание')
#     tags = ArrayField(base_field=models.CharField(max_length=20), verbose_name='Теги')
#
#     class Meta:
#         indexes = [
#             models.Index(fields=('name', 'description'), name='i_pgsrubric_name_description',
#                          opclasses=('varchar_pattern_ops', 'bpchar_pattern_ ops'))
#         ]
#
#
# class PGSProject(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     platform = ArrayField(base_field=ArrayField(
#         base_field=models.CharField(max_length=20)),
#         verbose_name='Используемые платформы')
#
# class PGSProject2(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     platform = HStoreField(verbose_name='Используемые платформы')
#
# class PGSProject3(models.Model):
#     name = CICharField(max_length=40, verbose_name='Название')
#     data = JSONField()

# class Comment(models.Model):
#     pass
#
#     class Meta:
#         permissions = (
#             ('hide_comment', 'Можно скрывать коммент'),
#         )