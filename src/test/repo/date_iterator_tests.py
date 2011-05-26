import nose
from nose.tools import *
from unittest import TestCase

from datetime import datetime, timedelta

from repo.date_iterator import DateIterator

class DateIteratorTests(TestCase):
    def test_date_iterator_returns_self_on_iter(self):
        d = DateIterator(datetime.now(), datetime.now())
        eq_(d, d.__iter__())

    def test_date_iterator_gives_first_date_as_start_date(self):
        start = datetime(2011, 3, 3)
        end = datetime(2011, 3, 4)
        d = DateIterator(start, end)
        first = d.next()
        eq_(start, first)
    
    def test_date_iterator_gives_next_date_30_days_by_default(self):
        start = datetime(2011, 3, 3)
        next = datetime(2011, 4, 2)
        end = datetime(2011, 4, 3)
        d = DateIterator(start, end)
        first = d.next()
        second = d.next()
        eq_(next, second)

    def test_date_iterator_gives_next_date_7_days(self):
        start = datetime(2011, 3, 3)
        next = datetime(2011, 3, 10)
        end = datetime(2011, 3, 14)
        d = DateIterator(start, end, delta=timedelta(days=7))
        first = d.next()
        second = d.next()
        eq_(next, second)
    
    @raises(StopIteration)
    def test_date_iterator_raises_stop_exception(self):
        start = datetime(2011, 3, 3)
        end = datetime(2011, 4, 1)
        d = DateIterator(start, end)
        first = d.next()
        second = d.next()

