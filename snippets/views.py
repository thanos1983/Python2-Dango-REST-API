from __future__ import print_function
from rest_framework import generics, status
from snippets.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, FileSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import mixins, views
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.response import Response
from snippets.modifications import FileProcesses
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
class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)
    # retrieve all fields from Snippet model
    queryset = Snippet.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data,
                                    context={'request': request})

        if serializer.is_valid():
            # save the data so the file can be created
            serializer.save(owner=self.request.user, )
            # instantiate the class the pass the request to be used by all methods
            file_obj = FileProcesses(request)
            # retrieve the data from the file
            list_of_data = file_obj.file_processing(settings.MEDIA_ROOT)
            data = '\n'.join(list_of_data)
            file_name = request.data.get('file')
            if file_name.name == 'keywords.txt':
                keywords = '\n'.join(list_of_data)
                # store the retrieved data
                serializer.save(code=keywords,
                                keywords=keywords)
            else:
                data = '\n'.join(list_of_data)
                # store the retrieved data
                serializer.save(code=data,)
            # store the retrieved data
            serializer.save(code=data, )
            # empty the dir of the data files
            file_obj.delete_data_files()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        '''
            # get filename
            file_name = request.data.get('file')
            if file_name.name == 'keywords.txt':
                # retrieve the data from the file
                list_of_data = file_obj.file_processing(settings.PROJECT_ROOT)
                keywords = '\n'.join(list_of_data)
                # store the retrieved data
                serializer.save(code=keywords,
                                keywords=keywords)
            else:
                list_of_data = file_obj.file_processing(settings.PROJECT_ROOT)
                data = '\n'.join(list_of_data)
                # store the retrieved data
                serializer.save(code=data,)
            # empty the dir of the data files
            file_obj.delete_data_files()'''


# class to be called when user is sending GET / POST requests through url <ip>:<port>/snippets/
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['code'] = "print('TEST')"
        serializer = SnippetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class to be called when user is sending GET / PUT / DELETE requests through url <ip>:<port>/snippets/(?P<pk>[0-9]+)/
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
