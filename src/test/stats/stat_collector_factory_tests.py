from nose.tools import *
from unittest import TestCase

from datetime import datetime, timedelta

from stats.stat_collector_factory import StatCollectorFactory
from stats.stat_collector_factory import StatConfigurationInvalidException
from stats.results_stat_collector import ResultsStatCollector
from files.file_package import FilePackageFactory

class StatCollectorFactoryTests(TestCase):
    def setUp(self):
        self.scf = StatCollectorFactory()

        self.mock_stat_factory = MockStatFactory()
        self.scf.set_stat_factory(self.mock_stat_factory)

        self.mock_repo_factory = MockRepositoryFactory()
        self.scf.set_repo_factory(self.mock_repo_factory)

        self.mock_results_stat_collector_factory = MockResultsStatCollectorFactory(None)
        self.scf.set_results_stat_collector_factory(self.mock_results_stat_collector_factory)

        self.mock_file_package_factory = MockFilePackageFactory()
        self.scf.set_file_package_factory(self.mock_file_package_factory)

    def test_stat_collector_factory_raises_exception_for_invalid_config_with_msg(self):
        didthrow = False
        try:
            self.scf.get_stat_collector({})
        except StatConfigurationInvalidException as e:
            didthrow = True
            ok_(str(e).startswith("Unable to find required configuration option"))
        ok_(didthrow)

    def test_stat_collector_factory_creates_proper_stat(self):
        statname = "my_favorite_stat"
        conf = { "statname": statname }
        stat = self.scf.create_stat_from_config(conf)
        eq_(statname, self.mock_stat_factory.get_last_stat_created())
        eq_(conf, self.mock_stat_factory.get_last_config_passed())

    def test_stat_collector_factory_creates_proper_repo(self):
        directory = "/home/mdrago/repository_lives_here"
        conf = { "repodir": directory }
        repo = self.scf.create_repo_from_config(conf)
        eq_(directory, self.mock_repo_factory.get_last_directory())

    def test_stat_collector_factory_creates_file_package(self):
        basedir = "/home/mdrago/repository_lives_here"
        subdir = "TestProject"
        conf = {}
        conf["repodir"] = basedir
        conf["dirs"] = [ subdir ]
        fp = self.scf.create_file_package_from_config(conf)
        eq_(subdir, self.mock_file_package_factory.get_file_package().dirs[0])

    def test_stat_collector_factory_creates_file_package_with_subdirs(self):
        basedir = "/home/mdrago/repository_lives_here"
        conf = {}
        conf["repodir"] = basedir
        conf["dirs"] = '*'
        fp = self.scf.create_file_package_from_config(conf)
        ok_(self.mock_file_package_factory.get_file_package().add_basedir_subdirs_was_called)

    def test_stat_collector_factory_creates_file_package_with_subdirs_when_dirs_omitted(self):
        basedir = "/home/mdrago/repository_lives_here"
        conf = {}
        conf["repodir"] = basedir
        fp = self.scf.create_file_package_from_config(conf)
        ok_(self.mock_file_package_factory.get_file_package().add_basedir_subdirs_was_called)

    def test_stat_collector_factory_creates_file_package_with_excluded_dirs(self):
        basedir = "/home/mdrago/repository_lives_here"
        conf = {}
        conf["repodir"] = basedir
        conf["exclude_dirs"] = ["dir1", "dir2"]
        fp = self.scf.create_file_package_from_config(conf)
        expected = set(("dir1", "dir2"))
        actual = set(self.mock_file_package_factory.get_file_package().excluded_dirs)
        eq_(expected, actual)

    def test_stat_collector_factory_creates_file_iterator(self):
        basedir = "/home/mdrago/repository_lives_here"
        subdir = "TestProject"
        conf = {}
        conf["repodir"] = basedir
        conf["dirs"] = [ subdir ]
        fi = self.scf.create_file_iterator_from_config(conf)
        eq_(1, len(fi.get_filepackages()))

    def test_stat_collector_factory_creates_matcher_glob(self):
        self.scf.set_file_package_factory(FilePackageFactory)
        glob = "*.java"
        basedir = "/home/mdrago/repository_lives_here"
        subdir = "TestProject"
        conf = {}
        conf["glob"] = glob
        conf["repodir"] = basedir
        conf["dirs"] = [ subdir ]
        fp = self.scf.create_file_package_from_config(conf)
        eq_(1, len(fp.file_matchers))
        eq_(glob, fp.file_matchers[0].glob)

    def test_stat_collector_factory_creates_start_time(self):
        current = datetime(2011, 5, 26, 7, 15, 0)
        self.scf.set_current_time(current)
        conf = {"start_time_delta": 7776000}
        start_time = self.scf.get_start_time_from_config(conf)
        eq_(datetime(2011, 2, 25, 7, 15, 0), start_time)

    def test_stat_collector_factory_creates_sample_time_interval(self):
        seconds = 2592000
        conf = {'sample_time_interval': seconds}
        expected = timedelta(seconds = seconds)
        actual = self.scf.get_sample_time_interval_from_config(conf)
        eq_(expected, actual)

    def test_stat_collector_factory_creates_results_stat_collector(self):
        conf = {'stattype': 'results', 'statname': 'mystat',
                'results_files': ['file1']}
        sc = self.scf.get_stat_collector(conf)
        eq_(MockResultsStatCollector, type(sc))

    def test_stat_collector_injects_results_file_names_in_to_collector(self):
        conf = {'stattype': 'results', 'statname': 'mystat',
                'results_files': ['file1', 'file2']}
        sc = self.scf.get_stat_collector(conf)
        rsc = self.mock_results_stat_collector_factory.get_results_stat_collector(None)
        eq_(['file1', 'file2'], rsc.files)

class MockResultsStatCollectorFactory(object):
    def __init__(self, stat):
        self.rsc = MockResultsStatCollector(stat)
    
    def get_results_stat_collector(self, stat):
        return self.rsc

class MockResultsStatCollector(object):
    def __init__(self, stat):
        self.files = None

    def set_results_files(self, files):
        self.files = files

    def get_stats(self):
        pass

class MockRepositoryFactory(object):
    def __init__(self):
        self.last_directory = None

    def get_repository(self, directory):
        self.last_directory = directory

    def get_last_directory(self):
        return self.last_directory

class MockStatFactory(object):
    def __init__(self):
        self.last_stat_created = None
        self.last_config_passed = None

    def get_stat(self, statname, conf=None):
        self.last_stat_created = statname
        self.last_config_passed = conf
        return None

    def get_last_stat_created(self):
        return self.last_stat_created
    
    def get_last_config_passed(self):
        return self.last_config_passed

    def return_non_existant_stat(self):
        self.get_stat_returns_non_existant = True

class MockFilePackageFactory(object):
    def __init__(self):
        self.mock = MockFilePackage()

    def get_file_package(self):
        return self.mock

class MockFilePackage(object):
    def __init__(self):
        self.dirs = []
        self.excluded_dirs = []
        self.add_basedir_subdirs_was_called = False

    def add_directory(self, directory):
        self.dirs.append(directory)

    def add_directories(self, *directories):
        for subdir in directories:
            self.add_directory(subdir)

    def exclude_directories(self, *directories):
        for subdir in directories:
            self.excluded_dirs.append(subdir)

    def add_file_matcher(self, fm):
        pass

    def set_basedir(self, basedir):
        pass

    def file_matchers(self):
        pass

    def add_basedir_subdirectories(self):
        self.add_basedir_subdirs_was_called = True

