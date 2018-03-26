from __future__ import print_function

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework import mixins, views
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAcceptable
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.reverse import reverse

from snippets.models import Snippet, Keyword
from snippets.modifications import FileProcesses
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, SnippetSerializerGui, KeywordSerializer
from snippets.serializers import UserSerializer
from thanosTest import settings


# GET to be called when user is or not logged in url <ip>:<port>
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


# class to be called when user is choosing url <ip>:<port>/snippets/(?P<pk>[0-9]+)/highlight/
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# class to be called when user is choosing url <ip>:<port>/users/
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class to be called when user is choosing url <ip>:<port>/users/(?P<pk>[0-9]+)/$
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class to be called when user is sending POST requests through url <ip>:<port>/upload/
class FileUploadViewKeywords(views.APIView):
    """
    List all keywords, or create a new input.
    """
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, format=None):
        keywords = Keyword.objects.all()
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = KeywordSerializer(data=request.data,
                                       context={'request': request})

        if serializer.is_valid():
            # check filename in case of keywords store keywords
            file_name = request.data.get('file')
            file_name.name = file_name.name.lower()
            if file_name.name == 'keywords.txt':
                # save the data so the file can be created
                serializer.save(owner=request.user, )
                # instantiate the class the pass the request to be used by all methods
                file_obj = FileProcesses(request)
                # retrieve the data from the file
                list_of_data = file_obj.file_processing(settings.MEDIA_ROOT)
                # create a string from list append \n new line character
                keywords = '\n'.join(list_of_data)
                # store the retrieved data
                serializer.save(owner=self.request.user,
                                keywords=keywords, )
                # empty the dir of the data files
                file_obj.delete_data_files()
            else:
                raise NotAcceptable("Please upload the correct file name e.g. 'keywords.txt'")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class to be called when user is sending POST requests through url <ip>:<port>/upload/
class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data,
                                       context={'request': request})

        if serializer.is_valid():
            # Retrieve latest keywords inserted by user
            db_dictionary = Keyword.objects.filter(owner=request.user).values('keywords').last()
            # If there are no keywords in data base raise 406 to the user and inform him
            if not bool(db_dictionary):
                raise NotAcceptable("There are no keywords in database. Please upload a 'keywords.txt' file.")
            # check filename in case of keywords store keywords
            file_name = request.data.get('file')
            file_name.name = file_name.name.lower()
            if file_name.name == 'keywords.txt':
                raise NotAcceptable("For file upload with file name e.g. 'keywords.txt' use url '/keywords/'")
            else:
                # save the data so the file can be created
                serializer.save(owner=request.user, )
                # instantiate the class the pass the request to be used by all methods
                file_obj = FileProcesses(request)
                # retrieve the data from the file
                list_of_data = file_obj.file_processing(settings.MEDIA_ROOT)
                information = '\n'.join(list_of_data)
                serializer.save(owner=self.request.user,
                                code=information,
                                keywords=db_dictionary['keywords'])
            # empty the dir of the data files
            file_obj.delete_data_files()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class to be called when user is sending GET / POST requests through url <ip>:<port>/snippets/
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializerGui

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = SnippetSerializerGui(data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            # retrieve latest keywords inserted by user
            db_dictionary = Snippet.objects.filter(owner=request.user).values('keywords').last()
            # if keywords found in database save and proceed
            if bool(db_dictionary):
                serializer.save(owner=request.user,
                                code=u"print('TEST')",
                                keywords=db_dictionary['keywords'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            raise NotAcceptable("There are no keywords in database. Please upload a keywords.txt file...")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class to be called when user is sending GET / DELETE requests through url <ip>:<port>/keywords/(?P<pk>[0-9]+)/
class KeywordDetail(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class to be called when user is sending GET / PUT / DELETE requests through url <ip>:<port>/snippets/(?P<pk>[0-9]+)/
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializerGui

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
