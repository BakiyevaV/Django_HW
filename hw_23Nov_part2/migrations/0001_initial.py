# Generated by Django 4.2.7 on 2023-11-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Icecream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
                ('mark', models.CharField(choices=[('Foodmaster', 'Foodmaster'), ('RusskiyStandart', 'RusskiyStandart'), ('Inmarko', 'Inmarko'), ('Nestle', 'Nestle'), ('Magnat', 'Magnat'), ('Bahroma', 'Bahroma')], max_length=15, verbose_name='торговая марка')),
                ('points', models.TextField(verbose_name='Точки реализации')),
            ],
            options={
                'verbose_name': 'Мореженое',
                'verbose_name_plural': 'Мореженое',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='stall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='ФИО')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
                ('icecream', models.ManyToManyField(to='hw_23Nov_part2.icecream')),
            ],
            options={
                'verbose_name': 'Киоск',
                'verbose_name_plural': 'Киоски',
                'ordering': ['name'],
            },
        ),
    ]
