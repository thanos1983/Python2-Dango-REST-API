from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# tuple of character(s)
CHARACTER_CHOICES = (
    (u"\u00AE", 'Registered Sign: ' + u"\u00AE"),
    (u"\u00A9", 'Copyright Sign: ' + u"\u00A9")
)

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    # This is the user of the text
    owner = models.ForeignKey('auth.User',
                              related_name='snippets',
                              on_delete=models.CASCADE)

    # Highlighted url (nice output)
    highlighted = models.TextField()

    # timestamp of the moment of the action
    created = models.DateTimeField(auto_now_add=True)

    # optional title of the text
    title = models.CharField(max_length=100,
                             blank=False,
                             default='Default Title',
                             help_text='Choose Text Title (Optional)')

    # text to be updated if we choose to input data manually
    code = models.TextField(blank=False,
                            default='Sample of Code',
                            help_text='Insert Here the Text to Format')

    # keywords list to be updated
    keywords = models.CharField(max_length=200,
                                blank=True,
                                default="Test\nTest2", )

    # line number on highlighted url
    linenos = models.BooleanField(default=False,
                                  help_text='Add Line Numbers in Viewing Highlighted url Link (Optional)')

    # choice of programing language for the highlighted url view
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                default='Python',
                                max_length=100,
                                help_text='Choose Programming Language in Viewing the Highlighted url Link (Optional)')

    # choice of characters to replace
    character = models.CharField(choices=CHARACTER_CHOICES,
                                 default=u"\u00AE",
                                 max_length=10,
                                 help_text='Choose Character to Replace')

    # another option of character representation on highlighted view
    style = models.CharField(choices=STYLE_CHOICES,
                             default='emacs',
                             max_length=10,
                             help_text='Choose Flavor of Text Editor in Viewing the Highlighted url Link (Optional)')

    # file to load that contains the lines
    file = models.FileField(blank=True,
                            null=False, )

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        # in which order to store the objects
        ordering = ('created',)
