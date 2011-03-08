import os
from fnmatch import fnmatch

class FileIterator(object):
    def __init__(self, directories, glob=None, basedir=None):
        self.set_directories(directories)
        self.set_glob(glob)
        self.set_base_directory(basedir)
    
    def set_directories(self, directories):
        self.directories = directories
    
    def set_glob(self, globtxt):
        self.glob = globtxt

    def set_base_directory(self, basedir):
        self.basedir = basedir

    def __iter__(self):
        return self.files().__iter__()
    
    def files(self):
        filelist = []
        for directory in self.directories:
            if self.basedir:
                directory = os.path.join(self.basedir, directory)
            for root, dirs, files in os.walk(directory):
                if self.glob:
                    files = filter(lambda f: fnmatch(f, self.glob), files)
                filelist += [os.path.join(root, f) for f in files]
        return filelist

