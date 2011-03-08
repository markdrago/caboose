import os
from fnmatch import fnmatch

class FileIterator(object):
    def __init__(self, directory, globtxt=None):
        self.directory = directory
        self.glob = globtxt
    
    def set_glob(self, globtxt):
        self.glob = globtxt

    def files(self):
        filelist = []
        for root, dirs, files in os.walk(self.directory):
            if self.glob:
                files = filter(lambda f: fnmatch(f, self.glob), files)
            filelist += [os.path.join(root, f) for f in files]
        return filelist

