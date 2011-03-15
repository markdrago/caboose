from os import path

class FilePackage(object):
    def __init__(self):
        self.directories = []
        self.file_matchers = []
        self.basedir = None
    
    def set_basedir(self, basedir):
        self.basedir = basedir
    
    def add_directory(self, directory):
        self.directories.append(directory)
    
    def add_directories(self, *args):
        for directory in args:
            self.add_directory(directory)
    
    def get_directories(self):
        if self.basedir:
            return [path.join(self.basedir, d) for d in self.directories]
        return self.directories

    def add_file_matcher(self, filematcher):
        self.file_matchers.append(filematcher)
    
    def add_file_matchers(self, *args):
        for filematcher in args:
            self.add_file_matcher(filematcher)
    
    def get_file_matchers(self):
        return self.file_matchers

