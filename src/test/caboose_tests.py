from nose.tools import *
from unittest import TestCase

from os import path

from ..stats.stat_runner import StatRunner
from caboose import Caboose

class CabooseTests(TestCase):
    def setUp(self):
        self.caboose = Caboose()

        self.config_parser = MockConfigParser()
        self.caboose.set_config_parser(self.config_parser)

        self.results_index = MockResultsIndex()
        self.caboose.set_results_index(self.results_index)

        self.stat_runner_factory = MockStatRunnerFactory()
        self.caboose.set_stat_runner_factory(self.stat_runner_factory)

    def test_set_configfile_calls_config_parser(self):
        self.caboose.set_configfile('hello/there.conf')
        eq_('hello/there.conf', self.config_parser.last_config_file)

    def test_create_results_index(self):
        statconf = { 'statname': 'stat1', 'outfile': 'outfilename', 'description': 'desc goes here' }
        conf = { 'output_directory': '/tmp/notused', 'stats' : [statconf] }
        self.caboose.config = conf
        self.caboose.run()

        eq_('/tmp/notused/outfilename', self.results_index.filename)
        eq_('desc goes here', self.results_index.desc)
        eq_('/tmp/notused', self.results_index.directory_passed)
    
    def test_exclude_item_from_results_index(self):
        statconf = { 'statname': 'stat1', 'include_in_results_index': False, 'outfile': 'outfilename', 'description': 'desc goes here' }
        conf = { 'output_directory': '/tmp/notused', 'stats' : [statconf] }
        self.caboose.config = conf
        self.caboose.run()
        
        eq_(None, self.results_index.desc)
        eq_(None, self.results_index.filename)

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

class MockConfigParser(object):
    def __init__(self):
        self.last_config_file = None

    def parse_file(self, config_file):
        self.last_config_file = config_file

class MockStatRunner(StatRunner):
    def run(self):
        pass

class MockStatRunnerFactory(object):
    def __init__(self):
        self.stat_runner = MockStatRunner()

    def get_stat_runner(self):
        return self.stat_runner

