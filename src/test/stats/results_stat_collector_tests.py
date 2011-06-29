from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp
from os import path

from stats.results_stat_collector import ResultsStatCollector

class ResultsStatCollectorTests(TestCase):
    def test_create_result_packages_from_files(self):
        #write out a json file
        self.directory = mkdtemp('-caboose-results-stat-collector-tests')
        filename = path.join(self.directory, 'results.json')
        with file(filename, 'w') as f:
            f.write('{\n  "stats": {\n    "1300489800000": 1234\n  }\n}')

        stat = MockResultsStat()
        results_files = [filename]
        self.rsc = ResultsStatCollector(stat, results_files)

        eq_(1, len(self.rsc.get_results()))
        eq_(1, self.rsc.get_results()[0].get_date_count())

        rmtree(self.directory)

class MockResultsStat(object):
    pass

