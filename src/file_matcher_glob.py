from fnmatch import fnmatch

class FileMatcherGlob(object):
    def __init__(self, glob):
        self.glob = glob

    def match(self, filename):
        return fnmatch(filename, self.glob)

