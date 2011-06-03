#!/usr/bin/python

import sys
from os import path

from config.config_parser import ConfigParser
from stats.stat_collector_factory import StatCollectorFactory
from results.results_index import ResultsIndex

class GettingBetter(object):
    def __init__(self):
        self.set_config_parser(ConfigParser())
        self.set_stat_collector_factory(StatCollectorFactory())
        self.set_results_index(ResultsIndex())

    def run(self):
        #TODO: get all of this ugliness out of here
        stat_collectors = self.create_stat_collectors(self.config)
        outfiles = self.get_outfile_locations(self.config)
        descriptions = self.get_stat_descriptions(self.config)
        for i in range(len(stat_collectors)):
            stat_collector = stat_collectors[i]
            outfile = outfiles[i]
            description = descriptions[i]
    
            results = stat_collector.get_stats()
            results.write_json_results(outfile)
            self.results_index.add_result(description, outfile)
        self.results_index.write_index(self.config['output_directory'])

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
        results = []
        output_dir = conf['output_directory']
        for statconf in conf['stats']:
            results.append(path.join(output_dir, statconf['outfile']))
        return results

    def get_stat_descriptions(self, conf):
        return [statconf['description'] for statconf in conf['stats']]

    def set_config_parser(self, parser):
        self.config_parser = parser

    def set_stat_collector_factory(self, scf):
        self.stat_collector_factory = scf

    def set_results_index(self, ri):
        self.results_index = ri

if __name__ == '__main__':
    gb = GettingBetter()
    gb.set_configfile(sys.argv[1])
    gb.run()

