from nose.tools import *
from unittest import TestCase

from stats.stat_factory import StatFactory
from stats.stat_factory import StatDoesNotExistException

from stats.stat_java_ncss import StatJavaNcss
from stats.stat_lines import StatLines
from stats.stat_java_mean_ccn import StatJavaMeanCcn
from stats.stat_java_ccn_func_count import StatJavaCcnFuncCount

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
        
    def test_create_stat_with_stat_conf(self):
        conf = { "statname": "java_mean_ccn", "ccn_limit": 10 }
        stat = self.sf.get_stat("java_ccn_func_count", conf)
        eq_(StatJavaCcnFuncCount, type(stat))
        eq_(10, stat.ccn_limit)

