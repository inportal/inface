# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.contrib.postgres.operations import HStoreExtension
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('alias', models.CharField(unique=True, max_length=50, verbose_name='user alias')),
                ('position', models.CharField(max_length=40, verbose_name='position', blank=True)),
                ('mobile', models.CharField(unique=True, max_length=12, verbose_name='mobile', blank=True)),
                ('email', models.EmailField(unique=True, max_length=200, verbose_name='email', db_index=True)),
                ('attr', django.contrib.postgres.fields.hstore.HStoreField(verbose_name='user attributes')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='administrator')),
                ('is_leader', models.BooleanField(default=False, verbose_name='leader')),
                ('is_virtual_user', models.BooleanField(default=False, verbose_name='virtual user')),
                ('no_login', models.BooleanField(default=False, verbose_name='not allowed login')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order by')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='department')),
                ('level', models.IntegerField(default=0, verbose_name='department level', editable=False)),
                ('rank', models.IntegerField(default=0, verbose_name='rank')),
                ('is_root', models.BooleanField(default=False, verbose_name='root')),
                ('is_removed', models.BooleanField(default=False, verbose_name='delete')),
                ('parent', models.ForeignKey(verbose_name='parent', blank=True, to='uc.Dept', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SysConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('param', django.contrib.postgres.fields.hstore.HStoreField(verbose_name='System Config Param')),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='dept',
            field=models.ForeignKey(verbose_name='department', to='uc.Dept', null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='master',
            field=models.ForeignKey(verbose_name='master user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
