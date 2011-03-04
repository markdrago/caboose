import nose
from nose.tools import *
from unittest import TestCase

from datetime import datetime

from repository import Repository
from repository_iterator import RepositoryIterator

class RepositoryIteratorTests(TestCase):
    def test_repository_iterator_switches_to_first_revision(self):
        date_revs = {
            datetime(2011, 1, 1): 0,
            datetime(2011, 2, 2): 1,
            datetime(2011, 3, 3): 2
        }
        
        di = date_revs.keys()
        di.sort()
        repo = MockDateRepository(date_revs)

        ri = RepositoryIterator(repo, date_iterator=di)
        ri.next()
        eq_(repo.latest_rev_requested, 0)

class MockDateRepository(Repository):
    def __init__(self, date_revs):
        self.date_revs = date_revs
        self.latest_rev_requested = None
    
    def get_revision_before_date(self, date):
        return self.date_revs[date]

    def switch_to_revision(self, rev):
        self.latest_rev_requested = rev

