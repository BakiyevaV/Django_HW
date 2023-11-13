from django.db import models

class Bb(models.Model):
    title = models.CharField(max_length=50,verbose_name='Товар')
    content = models.TextField(null=True, blank=True,verbose_name='Описание') #blank - достаточно
    price = models.FloatField(null=True, blank=True,verbose_name='Цена') #blank - достаточно, DecimalField - вместо float
    publiched = models.DateTimeField(auto_now_add = True, db_index=True,verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.title}'
    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-publiched']
