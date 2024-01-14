from django.db import models

class Tasks(models.Model):
    class Status(models.TextChoices):
        not_started = 'n', 'Не начато'
        done = 'd', 'Исполнено'
        in_progress = 'p', 'На исполнении'


    implementer = models.CharField(max_length=100, verbose_name="Исполнитель")
    author = models.CharField(max_length=100, verbose_name="Автор задачи")
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


