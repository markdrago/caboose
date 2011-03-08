import os

class FileIterator(object):
    def __init__(self, directory):
        self.directory = directory
    
    def files(self):
        filelist = []
        for root, dirs, files in os.walk(self.directory):
            filelist += [os.path.join(root, f) for f in files]
        return filelist

