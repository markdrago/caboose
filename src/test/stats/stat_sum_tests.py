from nose.tools import *
from unittest import TestCase

from stats.stat_sum import StatSum

class StatSumTests(TestCase):
    def setUp(self):
        self.stat = StatSum()
    
    def test_sum_works_in_common_case(self):
        eq_(120, self.stat.get_stat([80, 40]))
    
    def test_sum_works_with_many_stats(self):
        eq_(273, self.stat.get_stat([33, 100, 20, 50, 70]))

