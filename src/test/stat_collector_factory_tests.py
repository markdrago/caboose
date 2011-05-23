from nose.tools import *
from unittest import TestCase

from stat_collector_factory import StatCollectorFactory
from stat_collector_factory import StatConfigurationInvalidException

class StatCollectorFactoryTests(TestCase):
    def setUp(self):
        self.scf = StatCollectorFactory()

        self.mock_stat_factory = MockStatFactory()
        self.scf.set_stat_factory(self.mock_stat_factory)

        self.mock_repo_factory = MockRepositoryFactory()
        self.scf.set_repo_factory(self.mock_repo_factory)

        self.conf = {}
        for key in ("statname", "repodir"):
            self.conf[key] = "DEADBEEF"

    def test_stat_collector_raises_exception_for_invalid_config_with_msg(self):
        didthrow = False
        try:
            self.scf.get_stat_collector({})
        except StatConfigurationInvalidException as e:
            didthrow = True
            eq_("Unable to find statname configuration option", str(e))
        ok_(didthrow)

    def test_stat_collector_creates_proper_stat(self):
        statname = "my_favorite_stat"
        self.conf.update({ "statname": statname })
        sc = self.scf.get_stat_collector(self.conf)
        eq_(statname, self.mock_stat_factory.get_last_stat_created())

    def test_stat_collector_creates_proper_repo(self):
        directory = "/home/mdrago/repository_lives_here"
        self.conf.update({ "repodir": directory })
        sc = self.scf.get_stat_collector(self.conf)
        eq_(directory, self.mock_repo_factory.get_last_directory())

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

    def get_stat(self, statname):
        self.last_stat_created = statname
        return None

    def get_last_stat_created(self):
        return self.last_stat_created

    def return_non_existant_stat(self):
        self.get_stat_returns_non_existant = True

