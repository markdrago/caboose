from nose.tools import *
from unittest import TestCase

from getting_better import GettingBetter

class GettingBetterTests(TestCase):
    def setUp(self):
        self.gb = GettingBetter()
        self.config_parser = MockConfigParser()
        self.gb.set_config_parser(self.config_parser)
    
    def test_import_configfile_calls_load_source(self):
        self.gb.set_configfile('hello/there.conf')
        eq_('hello/there.conf', self.config_parser.last_config_file)

class MockConfigParser(object):
    def __init__(self):
        self.last_config_file = None

    def parse_file(self, config_file):
        self.last_config_file = config_file

