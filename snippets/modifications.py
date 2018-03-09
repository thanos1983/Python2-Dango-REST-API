import os


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

    def file_processing(self, path):
        # pass the path from the method to all functions
        self.path = path
        filename = self.request.data.get('file')
        return self.extract_data(filename.name)

    def extract_data(self, filename):
        with open(os.path.join(self.path, filename)) as f:
            lines = filter(None, (line.rstrip() for line in f))
        return lines

    def file_keywords(self, filename):
        # remove processed file
        os.remove(os.path.join(self.path, filename))
        return self.keywords

    def search_and_append(self):
        return self.path
