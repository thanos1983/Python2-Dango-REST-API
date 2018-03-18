from rest_framework import serializers
from snippets.models import Snippet, FileSnippet
from django.contrib.auth.models import User


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = FileSnippet
        fields = ('owner', 'file',)

        # keep this field hidden from the output (content of the file is stored in keywords)
        extra_kwargs = {
            'file': {'write_only': True}
        }


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight',
                                                     format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'character', 'style',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True,
                                                   view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets',)
