# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey_choice',
            name='mask',
            field=models.IntegerField(default=0),
        ),
    ]
