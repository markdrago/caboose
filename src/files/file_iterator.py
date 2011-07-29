import os
from fnmatch import fnmatch

class FileIteratorFactory(object):
    @classmethod
    def get_file_iterator(clazz, filepackages):
        return FileIterator(filepackages)

class FileIterator(object):
    def __init__(self, filepackages):
        self.set_filepackages(filepackages)
        self.excluded_path_globs = []
    
    def set_filepackages(self, filepackages):
        self.filepackages = filepackages

    def get_filepackages(self):
        return self.filepackages
    
    def exclude_path_globs(self, *globs):
        for glob in globs:
            self.excluded_path_globs.append(glob)

    def __iter__(self):
        return self.files().__iter__()
    
    #TODO: there must be a better way
    #TODO: excluded_path_globs should live in filepackage like filematchers do
    def files(self):
        filelist = []
        for filepackage in self.get_filepackages():
            for directory in filepackage.get_directories():
                for root, dirs, files in os.walk(directory):
                    #remove files which don't match filename glob
                    for filematcher in filepackage.get_file_matchers():
                        files = filter(lambda f: filematcher.match(f), files)

                    #get full paths of all files
                    fullpaths = [os.path.join(root, f) for f in files]

                    #remove files which do not exist (broken symlinks)
                    fullpaths = filter(lambda x: os.path.exists(x), fullpaths)

                    #remove files whose path matches an excluded_path_glob
                    for excluded_path_glob in self.excluded_path_globs:
                        fullpaths = filter(lambda x: not fnmatch(x, excluded_path_glob), fullpaths)

                    filelist += fullpaths

        return filelist

