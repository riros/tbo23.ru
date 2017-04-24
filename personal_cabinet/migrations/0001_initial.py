# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-13 09:25
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias_id', models.UUIDField(auto_created=True, default='00000000-0000-0000-0000-000000000000')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, max_length=12, verbose_name='Номер телефона')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='день рождения')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Отчество')),
                ('activation_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Код активации')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('name', models.CharField(help_text='номер лицевого счета', max_length=12, primary_key=True, serialize=False, verbose_name='Лицевой счет')),
                ('address_str', models.TextField(blank=True, null=True, verbose_name='Адрес')),
                ('fias_address_uuid', models.UUIDField(blank=True, null=True, verbose_name='Код адреса в системе fias')),
                ('date_open', models.DateField(verbose_name='дата открытия')),
                ('date_closed', models.DateField(blank=True, help_text='если пустое значение - значит бессрочный', null=True, verbose_name='Дата закрытия')),
                ('message', models.TextField(blank=True, null=True, verbose_name='сообщение пользователю')),
                ('euser', models.ForeignKey(default=1, help_text='Владелец лицевого счета', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Лицевой счет',
                'verbose_name_plural': 'Лицевые счета',
            },
        ),
        migrations.CreateModel(
            name='MonthBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='месяц расчета')),
                ('user_count', models.IntegerField(default=0, verbose_name='Количество проживающих')),
                ('price', models.FloatField(default=0, verbose_name='суммарная цена услуг с человека')),
                ('credit', models.FloatField(default=0, verbose_name='Начислено')),
                ('payment', models.FloatField(default=0, verbose_name='Оплачено')),
                ('debet', models.FloatField(default=0, verbose_name='Задолжность')),
                ('discounts', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, help_text='В рублях через запятую. Например: 20,50', null=True, size=None, verbose_name='Скидки')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal_cabinet.Account', verbose_name='Лицевой счет')),
            ],
            options={
                'verbose_name': 'Баланс по месяцам',
                'verbose_name_plural': 'Балансы по месяцам',
            },
        ),
    ]
