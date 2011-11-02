from fnmatch import fnmatch

class FileMatcherGlob(object):
    def __init__(self, globs):
        #globs can be a list of globs or a string of one glob
        if type(globs) == type(str()) or type(globs) == type(unicode()):
            self.globs = [globs]
        else:
            self.globs = globs

    def get_globs(self):
        return self.globs

    def match(self, filename):
        for glob in self.globs:
            if fnmatch(filename, glob):
                return True
        return False

