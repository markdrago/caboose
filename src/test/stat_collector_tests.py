import nose
from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp
from mercurial import commands
from datetime import datetime, timedelta

from mock_date_repository import MockDateRepository
from stat_collector import StatCollector    

class StatCollectorTests(TestCase):
    def test_stat_collector_gathers_single_simple_stat(self):
        date_revs = {datetime(2011, 1, 1): 0, datetime(2011, 1, 31): 1}
        repo = MockDateRepository(date_revs)
        
        sc = StatCollector(repo, timedelta(days=30),
                           ['file1'], stats=(SimpleStat(),),
                           end=datetime(2011, 1, 2))
        stats = sc.get_stats()
        eq_(1, stats.get_date_count())
        eq_(1, stats.get_result(datetime(2011, 1, 1), "simple"))

    def test_stat_collector_gathers_multiple_simple_stats(self):
        date_revs = {
            datetime(2011, 1, 1): 0,
            datetime(2011, 2, 2): 1,
            datetime(2011, 3, 3): 2
        }
        repo = MockDateRepository(date_revs)
        sc = StatCollector(repo, timedelta(days=30),
                           ['file1'], stats=(SimpleStat(),),
                           end=datetime(2011, 3, 4))
        stats = sc.get_stats()
        eq_(3, stats.get_date_count())
        eq_(1, stats.get_result(datetime(2011, 1, 1), "simple"))
        eq_(1, stats.get_result(datetime(2011, 1, 31), "simple"))
        eq_(1, stats.get_result(datetime(2011, 3, 2), "simple"))
    
    def test_stat_collector_handles_multiple_files(self):
        date_revs = {datetime(2011, 1, 1): 0, datetime(2011, 2, 2): 1}
        repo = MockDateRepository(date_revs)
        sc = StatCollector(repo, timedelta(days=30),
                           ['file1', 'file2'], stats=(SimpleStat(),),
                           end=datetime(2011, 1, 2))
        stats = sc.get_stats()
        eq_(1, stats.get_date_count())
        eq_(2, stats.get_result(datetime(2011, 1, 1), "simple"))

    def test_stat_collector_handles_multiple_stats(self):
        date_revs = {datetime(2011, 1, 1): 0, datetime(2011, 1, 31): 1}
        repo = MockDateRepository(date_revs)
        
        sc = StatCollector(repo, timedelta(days=30),
                           ['file1'], stats=(SimpleStat(), SimpleStat2()),
                           end=datetime(2011, 1, 2))
        stats = sc.get_stats()
        eq_(1, stats.get_date_count())
        eq_(1, stats.get_result(datetime(2011, 1, 1), "simple"))
        eq_(1, stats.get_result(datetime(2011, 1, 1), "simple2"))

class SimpleStat(object):
    def set_files(self, files):
        self.files = files

    def get_stat(self):
        return len(self.files)

    def get_name(self):
        return "simple"

class SimpleStat2(SimpleStat):
    def get_name(self):
        return "simple2"

