from nose.tools import *
from unittest import TestCase

from stats.stat_percentage import StatPercentage

class StatPercentageTests(TestCase):
    def setUp(self):
        self.stat = StatPercentage()
    
    def test_percentage_works_in_common_case(self):
        eq_(50, self.stat.get_stat([100, 200]))
    
    def test_percentage_stat_returns_a_float(self):
        result = self.stat.get_stat([33, 100])
        eq_(type(0.1), type(result))

    def test_percentage_stat_handles_zero_in_numerator(self):
        eq_(0, self.stat.get_stat([0, 250]))

    def test_percentage_stat_handles_zero_in_denominator(self):
        eq_(0, self.stat.get_stat([250, 0]))

    def test_percentage_stat_handles_small_denominator(self):
        eq_(150, self.stat.get_stat([300, 200]))

