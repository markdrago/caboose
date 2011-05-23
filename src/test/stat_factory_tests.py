from nose.tools import *
from unittest import TestCase

from stat_factory import StatFactory
from stat_factory import StatDoesNotExistException

from stat_java_ncss import StatJavaNcss
from stat_lines import StatLines
from stat_java_mean_ccn import StatJavaMeanCcn
from stat_java_ccn_func_count import StatJavaCcnFuncCount

class StatFactoryTests(TestCase):
    def setUp(self):
        self.sf = StatFactory()

    @raises(StatDoesNotExistException)
    def test_throws_stat_not_found_for_bogus_statname(self):
        stat = self.sf.get_stat("non_existent_stat")

    def test_create_java_ncss(self):
        stat = self.sf.get_stat("java_ncss")
        eq_(StatJavaNcss, type(stat))

    def test_create_lines(self):
        stat = self.sf.get_stat("lines")
        eq_(StatLines, type(stat))

    def test_create_java_mean_ccn(self):
        stat = self.sf.get_stat("java_mean_ccn")
        eq_(StatJavaMeanCcn, type(stat))

    def test_create_java_ccn_func_count(self):
        stat = self.sf.get_stat("java_ccn_func_count")
        eq_(StatJavaCcnFuncCount, type(stat))

