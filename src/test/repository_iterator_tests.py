import nose
from nose.tools import *
from unittest import TestCase

from datetime import datetime

from repository import Repository
from repository_iterator import RepositoryIterator

class RepositoryIteratorTests(TestCase):
    def setUp(self):
        self.date_revs = {
            datetime(2011, 1, 1): 0,
            datetime(2011, 2, 2): 1
        }
        
        self.di = self.date_revs.keys()
        self.di.sort()
        self.repo = MockDateRepository(self.date_revs)    
        self.ri = RepositoryIterator(self.repo, date_iterator=self.di)

    def test_repository_iterator_switches_to_first_revision(self):
        self.ri.next()
        eq_(self.repo.latest_rev_requested, 0)
    
    def test_repository_iterator_switches_to_second_revision(self):
        self.ri.next()
        self.ri.next()
        eq_(self.repo.latest_rev_requested, 1)
    
    @raises(StopIteration)
    def test_repository_iterator_throws_stop_iteration(self):
        self.ri.next()
        self.ri.next()
        self.ri.next()

class MockDateRepository(Repository):
    def __init__(self, date_revs):
        self.date_revs = date_revs
        self.latest_rev_requested = None
    
    def get_revision_before_date(self, date):
        return self.date_revs[date]

    def switch_to_revision(self, rev):
        self.latest_rev_requested = rev

