import os
from fnmatch import fnmatch

class FileIterator(object):
    def __init__(self, filepackages):
        self.set_filepackages(filepackages)
    
    def set_filepackages(self, filepackages):
        self.filepackages = filepackages

    def get_filepackages(self):
        return self.filepackages

    def __iter__(self):
        return self.files().__iter__()
    
    def files(self):
        filelist = []
        for filepackage in self.get_filepackages():
            for directory in filepackage.get_directories():
                for root, dirs, files in os.walk(directory):
                    for filematcher in filepackage.get_file_matchers():
                        files = filter(lambda f: filematcher.match(f), files)
                    filelist += [os.path.join(root, f) for f in files]
        return filelist

