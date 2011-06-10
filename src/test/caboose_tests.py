from nose.tools import *
from unittest import TestCase

from caboose import Caboose

class CabooseTests(TestCase):
    def setUp(self):
        self.caboose = Caboose()

        self.config_parser = MockConfigParser()
        self.caboose.set_config_parser(self.config_parser)

        self.stat_collector_factory = MockStatCollectorFactory()
        self.caboose.set_stat_collector_factory(self.stat_collector_factory)

        self.results_index = MockResultsIndex()
        self.caboose.set_results_index(self.results_index)
    
    def test_set_configfile_calls_config_parser(self):
        self.caboose.set_configfile('hello/there.conf')
        eq_('hello/there.conf', self.config_parser.last_config_file)

    def test_create_multiple_stat_collectors(self):
        stat1conf = { 'statname': 'stat1' }
        stat2conf = { 'statname': 'stat2' }
        conf = { 'stats' : [ stat1conf, stat2conf ] }
        scs = self.caboose.create_stat_collectors(conf)

        eq_(2, len(self.stat_collector_factory.confs))
        ok_(stat1conf in self.stat_collector_factory.confs)
        ok_(stat2conf in self.stat_collector_factory.confs)

    def test_get_multiple_outfile_locations(self):
        stat1conf = { 'outfile': 'file1' }
        stat2conf = { 'outfile': 'file2' }
        conf = { 'output_directory': '/tmp/notused',
                 'stats' : [ stat1conf, stat2conf ] }

        outfiles = self.caboose.get_outfile_locations(conf)
        eq_(['/tmp/notused/file1', '/tmp/notused/file2'], list(outfiles))

    def test_writes_results_to_json_outfile(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here' }
        conf = { 'stats' : [statconf], 'output_directory': '/tmp/notused' }
        self.caboose.config = conf
        self.caboose.run()

        res = self.stat_collector_factory.scs[0].results_package.outfile_requested
        eq_('/tmp/notused/outfilename', res)

    def test_create_results_index(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here' }
        conf = { 'output_directory': '/tmp/notused', 'stats' : [statconf] }
        self.caboose.config = conf
        self.caboose.run()

        eq_('/tmp/notused/outfilename', self.results_index.filename)
        eq_('desc goes here', self.results_index.desc)
        eq_('/tmp/notused', self.results_index.directory_passed)

class MockResultsIndex(object):
    def __init__(self):
        self.directory_passed = None
        self.filename = None
        self.desc = None

    def add_result(self, description, filename):
        self.desc = description
        self.filename = filename

    def write_index(self, directory):
        self.directory_passed = directory

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
