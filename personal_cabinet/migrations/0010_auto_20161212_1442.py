# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-12 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_cabinet', '0009_auto_20161212_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthbalance',
            name='date',
            field=models.DateField(auto_now=True, unique_for_month=True, verbose_name='месяц расчета'),
        ),
    ]