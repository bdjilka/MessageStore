# Generated by Django 2.1.5 on 2019-01-05 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='message',
            name='last_modify',
            field=models.DateField(auto_now=True, verbose_name='Дата последнего изменения'),
        ),
        migrations.AlterField(
            model_name='message',
            name='publish_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
