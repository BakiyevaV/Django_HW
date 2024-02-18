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








