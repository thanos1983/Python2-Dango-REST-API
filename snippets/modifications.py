import os
from thanosTest import settings
from django.core.files.storage import FileSystemStorage


class FileProcesses:

    def __init__(self, request):
        """
        instance variable unique to each instance
        request will be unique for all class functions
        :rtype: object
        """
        self.request = request
        self.keywords = None
        self.path = None

    def request_path_modification(self, file_path):
        # filename = self.request.data['file']
        self.path = file_path
        return os.path.join(settings.FILES_ROOT, str(self.request.user))

    def file_keywords(self, filename):
        # remove processed file
        os.remove(os.path.join(self.path, filename))
        return self.keywords

    def file_processing(self):
        filename = self.request.data['file']
        # create path
        self.path = os.path.join(settings.FILES_ROOT, str(self.request.user))
        # instantiate the class and pass the path
        # create path if does not exist
        self.create_dir_if_not_exist()
        # received file store and check if is located
        return self.store_file_in_dir(filename)

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
        # store file in allocated dir based on user
        fs = FileSystemStorage(location=self.path)
        fs.save(filename.name, filename)
        # check if file was successfully written
        if os.path.isfile(os.path.join(self.path, filename.name)):
            with open(os.path.join(self.path, filename.name)) as f:
                lines = filter(None, (line.rstrip() for line in f))
            os.remove(os.path.join(self.path, filename.name))
            return lines
