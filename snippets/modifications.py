import os
from thanosTest import settings
from rest_framework.response import Response


class FileProcesses:

    def __init__(self, request):
        """
        instance variable unique to each instance
        request will be unique for all class functions
        :rtype: object
        """
        self.request = request
        self.path = None

    def file_processing(self):
        filename = self.request.data['file']
        # create path
        self.path = os.path.join(settings.FILES_ROOT, str(self.request.user))
        # instantiate the class and pass the path
        # create path if does not exist
        self.create_dir_if_not_exist()
        # received file store and check if is located
        if self.store_file_in_dir(filename):
            return Response(filename.name, status=201)
        return Response(filename.name, status=404)

    def search_and_append(self):
        return self.path

    def create_dir_if_not_exist(self):
        """
        path is instantiated from the class (self.path)
        """
        # If path does not exist create dir
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def store_file_in_dir(self, filename):
        # Read binary file and write data in dir
        with open(os.path.join(self.path, filename.name), 'wb+') as destination:
            destination.write(filename.name)
        # check if file was successfully written
        if os.path.isfile(os.path.join(self.path, filename.name)):
            return True
        return False
