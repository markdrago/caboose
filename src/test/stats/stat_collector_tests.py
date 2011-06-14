import nose
from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp
from mercurial import commands
from datetime import datetime, timedelta

from test.repo.mock_date_repository import MockDateRepository
from stats.stat_collector import StatCollector    

class StatCollectorTests(TestCase):
    def test_stat_collector_gathers_single_simple_stat(self):
        date_revs = {datetime(2011, 1, 1): 0, datetime(2011, 1, 31): 1}
        repo = MockDateRepository(date_revs)

        sc = StatCollector(SimpleStat(), repo,
                           ['file1'], timedelta(days=30),
                           end=datetime(2011, 1, 2))
        stats = sc.get_stats()
        eq_(1, stats.get_date_count())
        eq_(1, stats.get_result(datetime(2011, 1, 1)))

    def test_stat_collector_gathers_multiple_simple_stats(self):
        date_revs = {
            datetime(2011, 1, 1): 0,
            datetime(2011, 2, 2): 1,
            datetime(2011, 3, 3): 2
        }
        repo = MockDateRepository(date_revs)
        sc = StatCollector(SimpleStat(), repo,
                           ['file1'], timedelta(days=30),
                           end=datetime(2011, 3, 4))
        stats = sc.get_stats()
        eq_(3, stats.get_date_count())
        eq_(1, stats.get_result(datetime(2011, 1, 1)))
        eq_(1, stats.get_result(datetime(2011, 1, 31)))
        eq_(1, stats.get_result(datetime(2011, 3, 2)))

    def test_stat_collector_handles_multiple_files(self):
        date_revs = {datetime(2011, 1, 1): 0, datetime(2011, 2, 2): 1}
        repo = MockDateRepository(date_revs)
        sc = StatCollector(SimpleStat(), repo,
                           ['file1', 'file2'], timedelta(days=30),
                           end=datetime(2011, 1, 2))
        stats = sc.get_stats()
        eq_(1, stats.get_date_count())
        eq_(2, stats.get_result(datetime(2011, 1, 1)))

class SimpleStat(object):
    @classmethod
    def get_name(clazz):
        return "simple"

    def set_files(self, files):
        self.files = files

    def get_stat(self):
        return len(self.files)

