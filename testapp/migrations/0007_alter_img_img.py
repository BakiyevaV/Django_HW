# Generated by Django 4.2.7 on 2024-02-29 14:05

from django.db import migrations, models
import testapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0006_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='img',
            field=models.ImageField(upload_to=testapp.models.get_timestamp_path, verbose_name='Изображение'),
        ),
    ]
