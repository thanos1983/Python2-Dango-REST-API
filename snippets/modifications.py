import os


class FileProcesses:

    def __init__(self, request):
        """
        instance variable unique to each instance
        request will be unique for all class functions
        :rtype: object
        """
        self.request = request
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

    def delete_data_files(self):
        for the_file in os.listdir(self.path):
            file_path = os.path.join(self.path, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def search_and_append(self):
        return self.path
