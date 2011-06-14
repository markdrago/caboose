from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp
from datetime import datetime
from os import path

from results.results_package import ResultsPackage

class ResultsPackageTests(TestCase):
    def setUp(self):
        self.rp = ResultsPackage()

    def test_result_package_holds_single_stat(self):
        dt = datetime(2011,03,18,18,44,0)
        self.rp.add_result(dt, 123)
        eq_(123, self.rp.get_result(dt))

    def test_result_package_overwrites_multiple_stats_one_time(self):
        dt = datetime(2011, 03, 18, 18, 52, 0)
        self.rp.add_result(dt, 1234)
        self.rp.add_result(dt, 2345)
        eq_(2345, self.rp.get_result(dt))
    
    def test_result_package_holds_multiple_stats_diff_time(self):
        dt1 = datetime(2011, 03, 18, 18, 52, 0)
        self.rp.add_result(dt1, 1234)
        dt2 = datetime(2011, 03, 18, 18, 54, 0)
        self.rp.add_result(dt2, 2345)
        eq_(1234, self.rp.get_result(dt1))
        eq_(2345, self.rp.get_result(dt2))
    
    def test_result_package_returns_number_of_dates_stored(self):
        dt1 = datetime(2011, 03, 18, 18, 52, 0)
        self.rp.add_result(dt1, 1234)
        eq_(1, self.rp.get_date_count())
        
        dt2 = datetime(2011, 03, 18, 18, 54, 0)
        self.rp.add_result(dt2, 2345)
        eq_(2, self.rp.get_date_count())

    def test_result_package_simple_json_output(self):
        dt = datetime(2011, 03, 18, 19, 10, 0)
        self.rp.add_result(dt, 1234)
        expected='{\n  "1300489800000": 1234\n}'
        eq_(expected, self.rp.get_json())
    
    def test_result_package_gives_list_of_dates(self):
        dt1 = datetime(2011, 04, 1, 19, 34, 0)
        self.rp.add_result(dt1, 1234)
        dt2 = datetime(2011, 04, 1, 19, 35, 0)
        self.rp.add_result(dt2, 2345)

        eq_(set(self.rp.get_dates()), set([dt1, dt2]))

    def test_result_package_writes_json_to_outfile(self):
        directory = mkdtemp('-caboose-results-package-tests')
        filename = path.join(directory, 'outfile')
        
        dt = datetime(2011, 03, 18, 19, 10, 0)
        self.rp.add_result(dt, 1234)
        self.rp.write_json_results(filename)

        with file(filename, "r") as f:
            written = f.read()

        expected='{\n  "1300489800000": 1234\n}'
        eq_(expected, written)
        rmtree(directory)

