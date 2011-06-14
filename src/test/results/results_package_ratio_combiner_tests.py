from nose.tools import *
from unittest import TestCase

from datetime import datetime

from results.results_package import ResultsPackage
from results.results_package_ratio_combiner import ResultsPackageRatioCombiner

class ResultsPackageTests(TestCase):
    def test_combine_simple_results_packages(self):
        dt = datetime(2011, 4, 1, 19, 24, 0)
        rp1 = ResultsPackage()
        rp1.add_result(dt, 5)
        rp2 = ResultsPackage()
        rp2.add_result(dt, 10)
        
        combiner = ResultsPackageRatioCombiner()
        rp3 = combiner.combine(rp1, rp2)
        eq_(0.5, rp3.get_result(dt))

