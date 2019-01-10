# Generated by Django 2.1.5 on 2019-01-05 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgapp', '0002_auto_20190105_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='message',
            name='last_modify',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения'),
        ),
        migrations.AlterField(
            model_name='message',
            name='publish_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]