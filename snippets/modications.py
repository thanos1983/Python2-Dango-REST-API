import os
import errno


class TextFieldAppend:

    def __init__(self, path):
        """
        instance variable unique to each instance
        :rtype: object
        """
        self.text_appended = []
        self.text_field_lines = []
        self.path = path

    def search_and_append(self):
        return self.path

    def file_transfer_check_dir(self, filename):
        try:
            os.makedirs(self.path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                # logger.error('Something went wrong: {}').format(e.errno)
                return False
            # logging.error('Something went wrong!')
        with open(self.path + filename, 'wb+') as destination:
            destination.write(filename)
        return True
