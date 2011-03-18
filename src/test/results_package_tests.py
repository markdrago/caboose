from nose.tools import *
from unittest import TestCase

from datetime import datetime

from results_package import ResultsPackage

class ResultsPackageTests(TestCase):
    def setUp(self):
        self.rp = ResultsPackage()

    def test_result_package_holds_single_stat(self):
        dt = datetime(2011,03,18,18,44,0)
        self.rp.add_result(dt, "simplestat", 123)
        eq_(123, self.rp.get_result(dt, "simplestat"))

    def test_result_package_holds_multiple_stats_one_time(self):
        dt = datetime(2011, 03, 18, 18, 52, 0)
        self.rp.add_result(dt, "simplestat", 1234)
        self.rp.add_result(dt, "simplestat2", 2345)
        eq_(1234, self.rp.get_result(dt, "simplestat"))
        eq_(2345, self.rp.get_result(dt, "simplestat2"))
    
    def test_result_package_holds_multiple_stats_diff_time(self):
        dt1 = datetime(2011, 03, 18, 18, 52, 0)
        self.rp.add_result(dt1, "simplestat", 1234)
        dt2 = datetime(2011, 03, 18, 18, 54, 0)
        self.rp.add_result(dt2, "simplestat2", 2345)
        eq_(1234, self.rp.get_result(dt1, "simplestat"))
        eq_(2345, self.rp.get_result(dt2, "simplestat2"))
    
    def test_result_package_gives_all_stats_for_date(self):
        dt = datetime(2011, 03, 18, 18, 52, 0)
        self.rp.add_result(dt, "simplestat", 1234)
        self.rp.add_result(dt, "simplestat2", 2345)
        expected = {"simplestat":1234, "simplestat2":2345}
        eq_(expected, self.rp.get_results_for_date(dt))

    def test_result_package_returns_number_of_dates_stored(self):
        dt1 = datetime(2011, 03, 18, 18, 52, 0)
        self.rp.add_result(dt1, "simplestat", 1234)
        eq_(1, self.rp.get_date_count())
        
        dt2 = datetime(2011, 03, 18, 18, 54, 0)
        self.rp.add_result(dt2, "simplestat2", 2345)
        eq_(2, self.rp.get_date_count())

    def test_resyult_package_simple_json_output(self):
        dt = datetime(2011, 03, 18, 19, 10, 0)
        self.rp.add_result(dt, "simplestat", 1234)
        expected='{"1300489800000": {"simplestat": 1234}}'
        eq_(expected, self.rp.get_json())

