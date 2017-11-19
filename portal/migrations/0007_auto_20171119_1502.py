# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_profile_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='education',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='workexp',
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='webmail',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
