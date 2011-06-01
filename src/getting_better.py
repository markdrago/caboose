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
        self.outfiles = self.get_outfile_locations(self.config)
        for i in range(len(self.stat_collectors)):
            stat_collector = self.stat_collectors[i]
            outfile = self.outfiles[i]

            results = stat_collector.get_stats()
            results.write_json_results(outfile)

    def create_stat_collectors(self, conf):
        stat_collectors = []
        for statconf in conf['stats']:
            sc = self.stat_collector_factory.get_stat_collector(statconf)
            stat_collectors.append(sc)
        return stat_collectors

    def set_configfile(self, configfile):
        self.configfile = configfile
        self.config = self.config_parser.parse_file(configfile)

    def get_outfile_locations(self, conf):
        return [statconf['outfile'] for statconf in conf['stats']]

    def set_config_parser(self, parser):
        self.config_parser = parser

    def set_stat_collector_factory(self, scf):
        self.stat_collector_factory = scf

if __name__ == '__main__':
    gb = GettingBetter()
    gb.set_configfile(sys.argv[1])
    gb.run()

