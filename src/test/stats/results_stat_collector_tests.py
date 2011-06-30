from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp
from os import path

from stats.results_stat_collector import ResultsStatCollector

class ResultsStatCollectorTests(TestCase):
    def test_create_result_packages_from_files(self):
        #write out a json file
        directory = mkdtemp('-caboose-results-stat-collector-tests')
        filename = path.join(directory, 'results.json')
        with file(filename, 'w') as f:
            f.write('{\n  "stats": {\n    "1300489800000": 1234\n  }\n}')

        stat = MockResultsStat()
        rsc = ResultsStatCollector(stat)

        rsc.set_results_files([filename])

        eq_(1, len(rsc.get_results()))
        eq_(1, rsc.get_results()[0].get_date_count())

        rmtree(directory)

    def test_get_stat(self):
        stat = MockResultsStat()
        rsc = ResultsStatCollector(stat)

        rp1 = MockResultsPackage()
        rp2 = MockResultsPackage()

        rsc.set_results([rp1, rp2])
        stats = rsc.get_stats()

        eq_([1, 2, 3], stats.get_dates())
        eq_(4, stats.get_result(1))
        eq_(8, stats.get_result(2))
        eq_(12, stats.get_result(3))

class MockResultsStat(object):
    def set_results_packages(self, results):
        self.results = results

    def get_stat(self, values):
        return sum(values)

class MockResultsPackage(object):
    def get_dates(self):
        return [1, 2, 3]

    def get_result(self, date):
        return date * 2

