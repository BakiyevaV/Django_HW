from django.db import models
# Create your models here.
class Icecream(models.Model):
    class TradeMark(models.TextChoices):
        Foodmaster = "Foodmaster","Foodmaster"
        RusskiyStandart = "RusskiyStandart","RusskiyStandart"
        Eczo = "Eczo","Eczo"
        Nestle = "Nestle","Nestle"
        Magnat = "Magnat","Magnat"
        Bahroma = "Bahroma","Bahroma"



    title = models.CharField(unique=True,null=False, blank=False, max_length=50, verbose_name="Наименование")
    mark = models.CharField(max_length=15, choices=TradeMark.choices, verbose_name="торговая марка")

    def __str__(self):
        return self.title

    class Meta:
        # доп настройки модели
        verbose_name_plural = 'Мореженое'
        verbose_name = 'Мореженое'
        ordering = ['title']

class Stall(models.Model):
    name = models.CharField(max_length=50,null=False, blank=False, verbose_name="Наименование")
    address = models.CharField(max_length=50,null=False, blank=False,  verbose_name="Адрес")
    icecream = models.ManyToManyField(Icecream)

    def __str__(self):
        return self.name

    class Meta:
        # доп настройки модели
        verbose_name_plural = 'Киоски'
        verbose_name = 'Киоск'
        ordering = ['name']
