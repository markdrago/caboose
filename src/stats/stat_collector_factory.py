from datetime import datetime, timedelta

from stat_factory import StatFactory
from repo_stat_collector import RepoStatCollector
from results_stat_collector import ResultsStatCollector
from repo.repository_factory import RepositoryFactory
from files.file_package import FilePackageFactory
from files.file_iterator import FileIteratorFactory
from files.file_matcher_glob import FileMatcherGlob
from results.results_package import ResultsPackage

class StatCollectorFactory(object):
    def __init__(self):
        self.set_stat_factory(StatFactory())
        self.set_repo_factory(RepositoryFactory)
        self.set_file_package_factory(FilePackageFactory)
        self.set_file_iterator_factory(FileIteratorFactory)
        self.set_current_time(datetime.now())
        self.set_results_stat_collector_factory(ResultsStatCollectorFactory())

    def get_stat_collector(self, conf):
        try:
            stat = self.create_stat_from_config(conf)
            if conf.get('stattype', None) == 'results':
                return self.get_results_stat_collector(stat, conf)
            else:
                return self.get_repo_stat_collector(stat, conf)
        except KeyError as e:
            raise StatConfigurationInvalidException("Unable to find required configuration option: %s" % str(e))

    def get_results_stat_collector(self, stat, conf):
        stat_collector = self.results_stat_collector_factory.get_results_stat_collector(stat)
        files = conf['results_files']
        stat_collector.set_results_files(files)
        return stat_collector

    def get_repo_stat_collector(self, stat, conf):
        repo = self.create_repo_from_config(conf)
        files = self.create_file_iterator_from_config(conf)
        start_time = self.get_start_time_from_config(conf)
        sample_interval = self.get_sample_time_interval_from_config(conf)

        return RepoStatCollector(stat, repo, files, sample_interval, start_time)

    def create_stat_from_config(self, conf):
        return self.stat_factory.get_stat(conf['statname'], conf)

    def create_repo_from_config(self, conf):
        return self.repo_factory.get_repository(conf['repodir'])

    def create_file_iterator_from_config(self, conf):
        fp = self.create_file_package_from_config(conf)
        fi = self.file_iterator_factory.get_file_iterator([fp])

        if 'exclude_path_globs' in conf:
            fi.exclude_path_globs(*conf['exclude_path_globs'])

        return fi

    def create_file_package_from_config(self, conf):
        fp = self.file_package_factory.get_file_package()
        fp.set_basedir(conf['repodir'])
        if 'dirs' not in conf or conf['dirs'] == '*':
            fp.add_basedir_subdirectories()
        else:
            fp.add_directories(*conf['dirs'])

        if 'exclude_dirs' in conf:
            fp.exclude_directories(*conf['exclude_dirs'])

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

    def set_results_stat_collector_factory(self, factory):
        self.results_stat_collector_factory = factory

    def set_file_package_factory(self, factory):
        self.file_package_factory = factory
    
    def set_file_iterator_factory(self, factory):
        self.file_iterator_factory = factory

class ResultsStatCollectorFactory(object):
    def get_results_stat_collector(self, stat):
        return ResultsStatCollector(stat)

class StatConfigurationInvalidException(Exception):
    pass

