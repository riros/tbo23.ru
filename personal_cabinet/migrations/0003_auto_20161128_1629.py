# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-28 13:29
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_cabinet', '0002_auto_20161128_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='euser',
            name='phones',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), null=True, size=None),
        ),
    ]
