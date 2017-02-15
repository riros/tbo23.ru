# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-22 12:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('personal_cabinet', '0017_auto_20161222_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_open',
            field=models.DateField(default=datetime.datetime(2016, 12, 22, 12, 1, 38, 920225, tzinfo=utc), verbose_name='дата открытия'),
        ),
        migrations.AlterField(
            model_name='monthbalance',
            name='date',
            field=models.DateField(verbose_name='месяц расчета'),
        ),
    ]