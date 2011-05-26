#!/usr/bin/python

import sys
import os
import imp

class GettingBetter(object):
    def __init__(self, importer=imp):
        self.importer = importer

    def run(self):
        mod = self.import_configfile()
        confobj = mod.GettingBetterConfig()
        confobj.run()
    
    def set_configfile(self, configfile):
        self.configfile = configfile

    def import_configfile(self):
        return self.importer.load_source('conf', self.configfile)

if __name__ == '__main__':
    configfile = sys.argv[1]
    gb = GettingBetter()
    gb.set_configfile(configfile)
    gb.run()
