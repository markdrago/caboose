from nose.tools import *
from unittest import TestCase

from stats.stat_runner import StatRunner

class StatRunnerTests(TestCase):
    def setUp(self):
        self.stat_runner = StatRunner()
    
        self.stat_collector_factory = MockStatCollectorFactory()
        self.stat_runner.set_stat_collector_factory(self.stat_collector_factory)

    def test_create_stat_collector(self):
        stat1conf = { 'statname': 'stat1' }
        self.stat_runner.set_conf(stat1conf)
        sc = self.stat_runner.create_stat_collector()

        eq_(1, len(self.stat_collector_factory.confs))
        ok_(stat1conf in self.stat_collector_factory.confs)

    def test_get_outfile_locations(self):
        self.stat_runner.set_conf({ 'outfile': 'file1' })

        self.stat_runner.set_output_directory('/tmp/notused')
        outfile = self.stat_runner.get_outfile_location()
        eq_('/tmp/notused/file1', outfile)

    def test_writes_results_to_json_outfile(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here' }
        self.stat_runner.set_conf(statconf)
        self.stat_runner.set_output_directory('/tmp/notused')
        self.stat_runner.run()

        res = self.stat_collector_factory.scs[0].results_package.outfile_requested
        eq_('/tmp/notused/outfilename', res)

class MockResultsPackage(object):
    def __init__(self):
        self.outfile_requested = None

    def write_json_results(self, outfile):
        self.outfile_requested = outfile

class MockStatCollector(object):
    def __init__(self):
        self.was_called = False
        self.results_package = MockResultsPackage()

    def get_stats(self):
        self.was_called = True
        return self.results_package

class MockStatCollectorFactory(object):
    def __init__(self):
        self.confs = []
        self.scs = []

    def get_stat_collector(self, conf):
        self.confs.append(conf)
        sc = MockStatCollector()
        self.scs.append(sc)
        return sc

