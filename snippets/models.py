from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.lexers import PythonLexer
from django.db import models


class Snippet(models.Model):
    lastTransaction = models.DateTimeField(auto_now_add=True)
    highlighted = models.TextField()
    textField = models.TextField(blank=False,
                                 help_text='Rows to modify.')
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    counterBefore = models.PositiveSmallIntegerField(default=0)
    counterAfter = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        self.highlighted = highlight(self.textField, PythonLexer(), HtmlFormatter(),)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ('lastTransaction',)

'''
from __future__ import unicode_literals

from django.db import models


class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    highlighted = models.TextField()
    code = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)'''
