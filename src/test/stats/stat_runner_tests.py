from nose.tools import *
from unittest import TestCase

from stats.stat_runner import StatRunner

class StatRunnerTests(TestCase):
    def setUp(self):
        self.stat_runner = StatRunner()
    
        self.stat_collector_factory = MockStatCollectorFactory()
        self.stat_runner.set_stat_collector_factory(self.stat_collector_factory)

        self.results_index = MockResultsIndex()
        self.stat_runner.set_results_index(self.results_index)

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
    
    def test_should_be_written_to_index(self):
        statconf = { 'include_in_results_index': False }
        self.stat_runner.set_conf(statconf)
        
        eq_(False, self.stat_runner.include_in_results_index())

    def test_include_in_results_index_default_to_true(self):
        eq_(True, self.stat_runner.include_in_results_index())

    def test_stat_runner_stores_stat_description(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here' }
        self.stat_runner.set_conf(statconf)
        eq_('desc goes here', self.stat_runner.get_description())

    def test_include_item_in_results_index(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here' }
        self.stat_runner.set_output_directory('/tmp/notused')
        self.stat_runner.set_conf(statconf)
        self.stat_runner.run()

        eq_('/tmp/notused/outfilename', self.results_index.filename)
        eq_('desc goes here', self.results_index.desc)

    def test_exclude_item_from_results_index(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here', 'include_in_results_index': False }
        self.stat_runner.set_output_directory('/tmp/notused')
        self.stat_runner.set_conf(statconf)
        self.stat_runner.run()

        eq_(None, self.results_index.desc)
        eq_(None, self.results_index.filename)
    
    def test_sets_description_in_results_package(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here'}
        self.stat_runner.set_output_directory('/tmp/notused')
        self.stat_runner.set_conf(statconf)
        self.stat_runner.run()

        eq_('desc goes here', self.stat_collector_factory.scs[0].results_package.description)

    def test_sets_datatype_in_results_package(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here', 'datatype': 'percentage' }
        self.stat_runner.set_output_directory('/tmp/notused')
        self.stat_runner.set_conf(statconf)
        self.stat_runner.run()

        eq_('percentage', self.stat_collector_factory.scs[0].results_package.datatype)

class MockResultsIndex(object):
    def __init__(self):
        self.filename = None
        self.desc = None

    def add_result(self, description, filename):
        self.desc = description
        self.filename = filename

class MockResultsPackage(object):
    def __init__(self):
        self.outfile_requested = None
        self.description = None
        self.datatype = None

    def set_description(self, desc):
        self.description = desc

    def set_datatype(self, datatype):
        self.datatype = datatype

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

