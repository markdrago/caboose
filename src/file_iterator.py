import os
from fnmatch import fnmatch

class FileIterator(object):
    def __init__(self, directories, globtxt=None):
        self.set_directories(directories)
        self.set_glob(globtxt)
    
    def set_directories(self, directories):
        self.directories = directories
    
    def set_glob(self, globtxt):
        self.glob = globtxt

    def files(self):
        filelist = []
        for directory in self.directories:
            for root, dirs, files in os.walk(directory):
                if self.glob:
                    files = filter(lambda f: fnmatch(f, self.glob), files)
                filelist += [os.path.join(root, f) for f in files]
        return filelist

