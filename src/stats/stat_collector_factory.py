from datetime import datetime, timedelta

from stat_factory import StatFactory
from stat_collector import StatCollector
from repo.repository_factory import RepositoryFactory
from files.file_package import FilePackage
from files.file_iterator import FileIterator
from files.file_matcher_glob import FileMatcherGlob
from results.results_package import ResultsPackage

class StatCollectorFactory(object):
    def __init__(self):
        self.set_stat_factory(StatFactory())
        self.set_repo_factory(RepositoryFactory)
        self.set_current_time(datetime.now())

    def get_stat_collector(self, conf):
        try:
            stat = self.create_stat_from_config(conf)
            repo = self.create_repo_from_config(conf)
            files = self.create_file_iterator_from_config(conf)
            start_time = self.get_start_time_from_config(conf)
            sample_interval = self.get_sample_time_interval_from_config(conf)
        except KeyError:
            raise StatConfigurationInvalidException("Unable to find required configuration option")

        return StatCollector(stat, repo, files, sample_interval, start_time)

    def create_stat_from_config(self, conf):
        return self.stat_factory.get_stat(conf['statname'], conf)

    def create_repo_from_config(self, conf):
        return self.repo_factory.get_repository(conf['repodir'])

    def create_file_iterator_from_config(self, conf):
        return FileIterator([self.create_file_package_from_config(conf)])

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

    def get_sample_time_interval_from_config(self, conf):
        return timedelta(seconds = conf['sample_time_interval'])

    def set_current_time(self, dt):
        self.current_time = dt

    def set_stat_factory(self, sf):
        self.stat_factory = sf

    def set_repo_factory(self, rf):
        self.repo_factory = rf

class StatConfigurationInvalidException(BaseException):
    pass

