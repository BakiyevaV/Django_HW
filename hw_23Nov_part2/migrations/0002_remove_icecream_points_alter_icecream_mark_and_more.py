# Generated by Django 4.2.7 on 2023-11-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hw_23Nov_part2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icecream',
            name='points',
        ),
        migrations.AlterField(
            model_name='icecream',
            name='mark',
            field=models.CharField(choices=[('Foodmaster', 'Foodmaster'), ('RusskiyStandart', 'RusskiyStandart'), ('Eczo', 'Eczo'), ('Nestle', 'Nestle'), ('Magnat', 'Magnat'), ('Bahroma', 'Bahroma')], max_length=15, verbose_name='торговая марка'),
        ),
        migrations.AlterField(
            model_name='stall',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Наименование'),
        ),
    ]
