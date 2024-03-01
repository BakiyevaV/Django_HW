# Generated by Django 4.2.7 on 2024-02-06 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0008_alter_bb_options_alter_bb_order_with_respect_to'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rubric',
            options={'ordering': ['order', 'name'], 'verbose_name': 'Рубрика', 'verbose_name_plural': 'Рубрики'},
        ),
        migrations.AddField(
            model_name='rubric',
            name='order',
            field=models.SmallIntegerField(db_index=True, default=0),
        ),
    ]
