from django.db import models
# Create your models here.
class Human(models.Model):
    class Gender(models.TextChoices):
        MALE = 'm', 'мужской'
        FEMALE = 'f', 'женский'
    name = models.CharField(primary_key=True, blank=False, max_length=50, verbose_name="ФИО")
    gender = models.CharField(max_length=1, choices=Gender.choices, verbose_name="Пол")
    age = models.PositiveIntegerField(verbose_name="Возраст")
    children_stat = models.BooleanField(default=False)
    children = models.CharField(max_length=50,blank=True, null=True, verbose_name="Дети")

    class Meta:
        # доп настройки модели
        verbose_name_plural = 'Люди'
        verbose_name = 'Человек'
        ordering = ['name','age']

class Child(models.Model):
    name = models.CharField(max_length=50, verbose_name="ФИО")
    gender = models.CharField(max_length=1, choices=Human.Gender.choices, verbose_name="Пол")
    age = models.PositiveIntegerField(verbose_name="Возраст")
    parent = models.ForeignKey('Human', on_delete=models.CASCADE, verbose_name='ФИО Родителя')

    class Meta:
        # доп настройки модели
        verbose_name_plural = 'Дети'
        verbose_name = 'Ребенок'
        ordering = ['name','parent']

