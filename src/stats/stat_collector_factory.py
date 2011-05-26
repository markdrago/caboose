from datetime import datetime, timedelta

from stat_factory import StatFactory
from repo.repository_factory import RepositoryFactory
from files.file_package import FilePackage
from files.file_iterator import FileIterator
from files.file_matcher_glob import FileMatcherGlob

class StatCollectorFactory(object):
    def __init__(self):
        self.set_stat_factory(StatFactory())
        self.set_repo_factory(RepositoryFactory)
        self.set_current_time(datetime.now())

    def get_stat_collector(self, conf):
        try:
            stat = self.stat_factory.get_stat(conf['statname'])
            repo = self.repo_factory.get_repository(conf['repodir'])
            files = self.create_file_iterator_from_config(conf)
        except KeyError:
            raise StatConfigurationInvalidException("Unable to find required configuration option")

    def create_file_iterator_from_config(self, conf):
        return FileIterator(self.create_file_package_from_config)

    def create_file_package_from_config(self, conf):
        fp = FilePackage()
        fp.set_basedir(conf['repodir'])
        fp.add_directories(*conf['dirs'])

        if 'glob' in conf:
            fm = FileMatcherGlob(conf['glob'])
            fp.add_file_matcher(fm)

        return fp

    def get_start_time_from_config(self, conf):
        delta = timedelta(seconds = conf['start_time_delta'])
        return self.current_time - delta

    def set_current_time(self, dt):
        self.current_time = dt

    def set_stat_factory(self, sf):
        self.stat_factory = sf

    def set_repo_factory(self, rf):
        self.repo_factory = rf

class StatConfigurationInvalidException(BaseException):
    pass

