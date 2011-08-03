#!/usr/bin/python

import sys

from config.config_parser import ConfigParser
from results.results_index import ResultsIndex
from stats.stat_runner import StatRunner

class Caboose(object):
    def __init__(self):
        self.set_config_parser(ConfigParser())
        self.set_results_index(ResultsIndex())
        self.set_stat_runner_factory(StatRunnerFactory())

    def run(self):
        for runner in self.get_stat_runners():
            runner.run()
        self.results_index.write_index(self.get_output_directory())

    def set_configfile(self, configfile):
        self.configfile = configfile
        self.config = self.config_parser.parse_file(configfile)

    def get_stat_runners(self):
        runners = []
        for statconf in self.config['stats']:
            runner = self.stat_runner_factory.get_stat_runner()
            runner.set_conf(statconf)
            runner.set_output_directory(self.get_output_directory())
            runner.set_results_index(self.results_index)
            runners.append(runner)
        return runners

    def get_output_directory(self):
        return self.config['output_directory']

    def set_config_parser(self, parser):
        self.config_parser = parser

    def set_results_index(self, ri):
        self.results_index = ri

    def set_stat_runner_factory(self, srf):
        self.stat_runner_factory = srf

class StatRunnerFactory(object):
    def get_stat_runner(self):
        return StatRunner()

if __name__ == '__main__':
    caboose = Caboose()
    caboose.set_configfile(sys.argv[1])
    caboose.run()

