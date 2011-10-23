import re

class FilePreProcessRegex(object):
    def __init__(self):
        self.full_file_contents = ""
        self.pattern = r'@Transactional'

    @classmethod
    def get_name(clazz):
        return 'regex'

    def set_input(self, contents):
        self.full_file_contents = contents
    
    def get_output(self):
        result = ""
        for line in self.full_file_contents.split("\n"):

            #TODO: let regex specify this
            line = line.lower()

            if re.search(self.pattern, line) is not None:
                result += line + "\n"
        return result

