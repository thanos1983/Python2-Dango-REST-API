# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from django.db import models


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()

    class Meta:
        ordering = ('created',)
