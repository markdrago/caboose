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

        self.stat_runner_factory = MockStatRunnerFactory()
        self.caboose.set_stat_runner_factory(self.stat_runner_factory)

    def test_set_configfile_calls_config_parser(self):
        self.caboose.set_configfile('hello/there.conf')
        eq_('hello/there.conf', self.config_parser.last_config_file)

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

