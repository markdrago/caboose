#!/usr/bin/python

import sys

from config.config_parser import ConfigParser
from stats.stat_collector_factory import StatCollectorFactory

class GettingBetter(object):
    def __init__(self):
        self.set_config_parser(ConfigParser())
        self.set_stat_collector_factory(StatCollectorFactory())

    def run(self):
        self.stat_collectors = self.create_stat_collectors(self.config)

    def create_stat_collectors(self, conf):
        stat_collectors = []
        for statconf in conf['stats']:
            sc = self.stat_collector_factory.get_stat_collector(statconf)
            stat_collectors.append(sc)
        return stat_collectors
    
    def set_configfile(self, configfile):
        self.configfile = configfile
        self.config = self.config_parser.parse_file(configfile)

    def set_config_parser(self, parser):
        self.config_parser = parser

    def set_stat_collector_factory(self, scf):
        self.stat_collector_factory = scf

if __name__ == '__main__':
    gb = GettingBetter()
    gb.set_configfile(sys.argv[1])
    gb.run()

