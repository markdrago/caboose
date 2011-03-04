import nose
from nose.tools import *
from unittest import TestCase

from datetime import datetime

from repository_iterator import RepositoryIterator
from mock_date_repository import MockDateRepository

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
        date = self.ri.next()
        eq_(self.repo.latest_rev_requested, 0)
        eq_(datetime(2011, 1, 1), date)
    
    def test_repository_iterator_switches_to_second_revision(self):
        self.ri.next()
        date = self.ri.next()
        eq_(self.repo.latest_rev_requested, 1)
        eq_(datetime(2011, 2, 2), date)
    
    @raises(StopIteration)
    def test_repository_iterator_throws_stop_iteration(self):
        self.ri.next()
        self.ri.next()
        self.ri.next()

