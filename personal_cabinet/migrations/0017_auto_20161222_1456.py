# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-22 11:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('personal_cabinet', '0016_auto_20161222_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_closed',
            field=models.DateField(blank=True, help_text='если пустое значение - значит бессрочный', null=True, verbose_name='Дата закрытия'),
        ),
        migrations.AlterField(
            model_name='account',
            name='date_open',
            field=models.DateField(default=datetime.datetime(2016, 12, 22, 11, 56, 57, 636403, tzinfo=utc), verbose_name='дата открытия'),
        ),
        migrations.AlterField(
            model_name='account',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='сообщение пользователю'),
        ),
        migrations.AlterField(
            model_name='euser',
            name='middle_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='monthbalance',
            name='date',
            field=models.DateField(unique_for_month=True, verbose_name='месяц расчета'),
        ),
    ]
