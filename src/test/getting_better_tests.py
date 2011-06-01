from nose.tools import *
from unittest import TestCase

from getting_better import GettingBetter

class GettingBetterTests(TestCase):
    def setUp(self):
        self.gb = GettingBetter()

        self.config_parser = MockConfigParser()
        self.gb.set_config_parser(self.config_parser)

        self.stat_collector_factory = MockStatCollectorFactory()
        self.gb.set_stat_collector_factory(self.stat_collector_factory)
    
    def test_set_configfile_calls_config_parser(self):
        self.gb.set_configfile('hello/there.conf')
        eq_('hello/there.conf', self.config_parser.last_config_file)

    def test_create_multiple_stat_collectors(self):
        stat1conf = { 'statname': 'stat1' }
        stat2conf = { 'statname': 'stat2' }
        conf = { 'stats' : [ stat1conf, stat2conf ] }
        scs = self.gb.create_stat_collectors(conf)

        eq_(2, len(self.stat_collector_factory.confs))
        ok_(stat1conf in self.stat_collector_factory.confs)
        ok_(stat2conf in self.stat_collector_factory.confs)

    def test_get_multiple_outfile_locations(self):
        stat1conf = { 'outfile': 'file1' }
        stat2conf = { 'outfile': 'file2' }
        conf = { 'stats' : [ stat1conf, stat2conf ] }

        outfiles = self.gb.get_outfile_locations(conf)
        eq_(['file1', 'file2'], list(outfiles))

    def test_writes_results_to_json_outfile(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename' }
        conf = { 'stats' : [statconf] }
        self.gb.config = conf
        self.gb.run()

        res = self.stat_collector_factory.scs[0].results_package.outfile_requested
        eq_('outfilename', res)

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

class MockConfigParser(object):
    def __init__(self):
        self.last_config_file = None

    def parse_file(self, config_file):
        self.last_config_file = config_file

