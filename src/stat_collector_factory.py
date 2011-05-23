from stat_factory import StatFactory
from repository_factory import RepositoryFactory

class StatCollectorFactory(object):
    def __init__(self):
        self.set_stat_factory(StatFactory())
        self.set_repo_factory(RepositoryFactory)

    def get_stat_collector(self, conf):
        try:
            stat = self.stat_factory.get_stat(conf['statname'])
            repo = self.repo_factory.get_repository(conf['repodir'])
        except KeyError:
            raise StatConfigurationInvalidException("Unable to find statname configuration option")

    def set_stat_factory(self, sf):
        self.stat_factory = sf

    def set_repo_factory(self, rf):
        self.repo_factory = rf

class StatConfigurationInvalidException(BaseException):
    pass

