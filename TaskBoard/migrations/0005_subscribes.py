# Generated by Django 5.0.1 on 2024-01-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskBoard', '0004_alter_tasks_options_alter_tasks_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30, verbose_name='Mейл')),
            ],
        ),
    ]
