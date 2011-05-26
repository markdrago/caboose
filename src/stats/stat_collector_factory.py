from stat_factory import StatFactory
from repo.repository_factory import RepositoryFactory
from file_package import FilePackage
from file_iterator import FileIterator

class StatCollectorFactory(object):
    def __init__(self):
        self.set_stat_factory(StatFactory())
        self.set_repo_factory(RepositoryFactory)

    def get_stat_collector(self, conf):
        try:
            stat = self.stat_factory.get_stat(conf['statname'])
            repo = self.repo_factory.get_repository(conf['repodir'])
            files = self.create_file_iterator_from_config(conf)
        except KeyError:
            raise StatConfigurationInvalidException("Unable to find statname configuration option")

    def create_file_iterator_from_config(self, conf):
        return FileIterator(self.create_file_package_from_config)

    def create_file_package_from_config(self, conf):
        fp = FilePackage()
        fp.set_basedir(conf['repodir'])
        fp.add_directories(*conf['dirs'])
        return fp

    def set_stat_factory(self, sf):
        self.stat_factory = sf

    def set_repo_factory(self, rf):
        self.repo_factory = rf

class StatConfigurationInvalidException(BaseException):
    pass

