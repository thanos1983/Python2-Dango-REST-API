import os
import string


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
            data = filter(None, (line.rstrip() for line in f))
        return data

    def delete_data_files(self):
        for the_file in os.listdir(self.path):
            file_path = os.path.join(self.path, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def replace_all(self, line, dic):
        for i, j in dic.iteritems():
            line = line.replace(i, j)
        return line

    def search_and_append(self, data, keywords, character):
        # convert string to hash key old keyword value keyword appended with character
        keyword_dict = dict((keyword, keyword + character) for keyword in keywords.split('\n'))
        # iterate over the list so we can process one by one the lines
        new_string_list = []
        for line in data:
            new_string_list.append(self.replace_all(line, keyword_dict))
        return new_string_list
