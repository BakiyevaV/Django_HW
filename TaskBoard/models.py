from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

class Tasks(models.Model):
    class Status(models.TextChoices):
        not_started = 'n', 'Не начато'
        done = 'd', 'Исполнено'
        in_progress = 'p', 'На исполнении'


    implementer = models.CharField(max_length=100, verbose_name="Исполнитель", null=True, blank=True)
    author = models.CharField(max_length=100, verbose_name="Автор задачи", null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    deadline = models.DateField(db_index=True, verbose_name="Срок исполнения")
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата публикации")
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.not_started, verbose_name="Статус")
    done_date = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name="Дата исполнения")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Задачи'
        verbose_name = 'Задача'
        ordering = ['-status','-deadline']


class Subscribes(models.Model):
    email = models.CharField(max_length=30, verbose_name="Mейл")

class Icecream(models.Model):

    class Package(models.TextChoices):
        Cup = 'cup', 'стаканчик'
        Cone = 'cone', 'рожок'
        Brick = 'brick', 'брикет'
        Tube = 'tube', 'туба '
        Box = 'box', 'коробка'
        Pouch = 'pouch', 'пакетик'
        Foil = 'foil', 'фольга'
        Plastic_container = 'plastic_container', 'пластиковый контенер'
        Paper_container = 'paper container', 'бумажный контенер'
        Balls = 'balls', 'шарик'

    name = models.CharField(max_length=40, verbose_name="Тороговое наименование")
    fabricator = models.CharField(max_length=40, verbose_name="Производитель")
    composition = models.CharField(max_length=500, verbose_name="Состав", null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Стоимость")
    package = models.CharField(max_length=20, choices=Package.choices, default=Package.Balls, verbose_name="Упаковка")
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Вес нетто", default=200.00)
    expiration_date_in_days = models.IntegerField(verbose_name="Срок употребления", default=30)

    class Meta:
        verbose_name_plural = 'Мороженое'
        verbose_name = 'Мороженое'
        ordering = ['name']

    def __str__(self):
        return self.name

class Vendors(models.Model):
    name = models.CharField(max_length=40, verbose_name="Наименование продавца")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    number = models.CharField(max_length=200, verbose_name="Номер для связи", blank=True, null=True)
    icecream_pl = models.ManyToManyField(Icecream, through='Vendors_Icecream', through_fields=('vendor',
                                                                                               'icecream_position'))
    class Meta:
        verbose_name_plural = 'Продавцы'
        verbose_name = 'Продавец'
        ordering = ['name']

    def __str__(self):
        return self.name

class Vendors_Icecream(models.Model):
    icecream_position = models.ForeignKey(Icecream, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

class PassValidator():
    def __init__(self, password):
        self.password = password
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

    def __call__(self, value):
        if len(value) < 6 or not self.check_item():
            raise ValidationError('Пароль должен содержать не менее 6 символов и не менее одной прописной буквы, строчной буквы, цифры и специального знака',
                                  code='out_of_range', params={'password': value})


class Clients(models.Model):
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=30, unique=True, validators=[validators.RegexValidator(regex='\w[\w\.-]*\w+@\w[\w\.]*\.[a-zA-Z]{2,3}')], error_messages= {'invalid':'Введите корректный адрес электронной почты'})
    birth_date = models.DateField()
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'

class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username









