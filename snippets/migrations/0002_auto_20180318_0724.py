# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-18 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='keywords',
            field=models.CharField(blank=True, default=b'Test\nTest2', max_length=200),
        ),
    ]
