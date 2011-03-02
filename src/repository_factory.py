from os import path

from mercurial_repository import MercurialRepository

class RepositoryFactory(object):
    @classmethod
    def get_repository(klass, directory):
        if path.isdir(path.join(directory, '.hg')):
            return MercurialRepository(directory)
        raise Exception("No repository found in directory: %s" % directory)
