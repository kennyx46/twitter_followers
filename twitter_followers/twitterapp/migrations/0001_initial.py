# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('screen_name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('str_id', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=100)),
            ],
        ),
    ]
