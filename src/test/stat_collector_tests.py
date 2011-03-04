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
                           dirs=('.',), stat_classes=(SimpleStat,),
                           end=datetime(2011, 1, 2))
        stats = sc.get_stats()
        eq_(1, len(stats.keys()))
        eq_(1, stats[datetime(2011, 1, 1)])

    def test_stat_collector_gathers_multiple_simple_stats(self):
        date_revs = {
            datetime(2011, 1, 1): 0,
            datetime(2011, 2, 2): 1,
            datetime(2011, 3, 3): 2
        }
        repo = MockDateRepository(date_revs)
        sc = StatCollector(repo, timedelta(days=30),
                           dirs=('.',), stat_classes=(SimpleStat,),
                           end=datetime(2011, 3, 4))
        stats = sc.get_stats()
        eq_(3, len(stats.keys()))
        eq_(1, stats[datetime(2011, 1, 1)])
        eq_(1, stats[datetime(2011, 1, 31)])
        eq_(1, stats[datetime(2011, 3, 2)])
    
    def test_stat_collector_handles_multiple_directories(self):
        date_revs = {datetime(2011, 1, 1): 0, datetime(2011, 2, 2): 1}
        repo = MockDateRepository(date_revs)
        sc = StatCollector(repo, timedelta(days=30),
                           dirs=('.', 'another'), stat_classes=(SimpleStat,),
                           end=datetime(2011, 1, 2))
        stats = sc.get_stats()
        eq_(1, len(stats.keys()))
        eq_(2, stats[datetime(2011, 1, 1)])

class SimpleStat(object):
    def __init__(self, dirs):
        self.dirs = dirs
    
    def get_stat(self):
        return len(self.dirs)

