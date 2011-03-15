class FilePackage(object):
    def __init__(self):
        self.directories = []
        self.file_matchers = []
    
    def add_directory(self, directory):
        self.directories.append(directory)
    
    def add_directories(self, *args):
        for directory in args:
            self.add_directory(directory)
    
    def get_directories(self):
        return self.directories

    def add_file_matcher(self, filematcher):
        self.file_matchers.append(filematcher)
    
    def add_file_matchers(self, *args):
        for filematcher in args:
            self.add_file_matcher(filematcher)
    
    def get_file_matchers(self):
        return self.file_matchers

