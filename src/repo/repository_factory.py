from os import path

from mercurial_repository import MercurialRepository
from git_repository import GitRepository

class RepositoryFactory(object):
    @classmethod
    def get_repository(klass, directory):
        if path.isdir(path.join(directory, '.hg')):
            return MercurialRepository(directory)
        elif path.isdir(path.join(directory, '.git')):
            return GitRepository(directory)
        raise Exception("No repository found in directory: %s" % directory)

