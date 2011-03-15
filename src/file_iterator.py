import os
from fnmatch import fnmatch

class FileIterator(object):
    def __init__(self, filepackages, basedir=None):
        self.set_filepackages(filepackages)
        self.set_base_directory(basedir)
    
    def set_filepackages(self, filepackages):
        self.filepackages = filepackages

    def set_base_directory(self, basedir):
        self.basedir = basedir

    def __iter__(self):
        return self.files().__iter__()
    
    def files(self):
        filelist = []
        for filepackage in self.filepackages:
            for directory in filepackage.get_directories():
                if self.basedir:
                    directory = os.path.join(self.basedir, directory)
                for root, dirs, files in os.walk(directory):
                    for filematcher in filepackage.get_file_matchers():
                        files = filter(lambda f: filematcher.match(f), files)
                    filelist += [os.path.join(root, f) for f in files]
        return filelist

