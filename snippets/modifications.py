import os


class FileProcesses:

    def __init__(self, path):
        """
        instance variable unique to each instance
        path will be common for all class functions
        :rtype: object
        """
        self.path = path

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
        with open(os.path.join(self.path, filename), 'wb+') as destination:
            destination.write(filename)
        # check if file was successfully written
        if os.path.isfile(os.path.join(self.path, filename)):
            return True
        return False
