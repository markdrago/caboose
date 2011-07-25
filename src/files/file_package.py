import os
import stat

class FilePackageFactory(object):
    @classmethod
    def get_file_package(clazz):
        return FilePackage()

class FilePackage(object):
    def __init__(self):
        self.directories = []
        self.excluded_directories = []
        self.file_matchers = []
        self.basedir = None
    
    def set_basedir(self, basedir):
        self.basedir = basedir
    
    def add_directory(self, directory):
        self.directories.append(directory)
    
    def add_directories(self, *args):
        for directory in args:
            self.add_directory(directory)

    def add_basedir_subdirectories(self):
        for subdir in os.listdir(self.basedir):
            statinfo = os.stat(os.path.join(self.basedir, subdir))
            if stat.S_ISDIR(statinfo[stat.ST_MODE]):
                self.add_directory(subdir)

    def exclude_directory(self, directory):
        self.excluded_directories.append(directory)
    
    def exclude_directories(self, *args):
        for directory in args:
            self.exclude_directory(directory)

    def get_directories(self):
        dirs = [d for d in self.directories if d not in self.excluded_directories]
        if self.basedir:
            return [os.path.join(self.basedir, d) for d in dirs]
        return dirs

    def add_file_matcher(self, filematcher):
        self.file_matchers.append(filematcher)
    
    def add_file_matchers(self, *args):
        for filematcher in args:
            self.add_file_matcher(filematcher)
    
    def get_file_matchers(self):
        return self.file_matchers

