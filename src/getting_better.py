#!/usr/bin/python

import sys

from config.config_parser import ConfigParser

class GettingBetter(object):
    def __init__(self):
        self.set_config_parser(ConfigParser())

    def run(self):
        confobj.run()
    
    def set_configfile(self, configfile):
        self.configfile = configfile
        self.config = self.config_parser.parse_file(configfile)

    def set_config_parser(self, parser):
        self.config_parser = parser

if __name__ == '__main__':
    gb = GettingBetter()
    gb.set_configfile(sys.argv[1])
    gb.run()

