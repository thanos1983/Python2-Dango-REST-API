# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-09 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='keywords',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
