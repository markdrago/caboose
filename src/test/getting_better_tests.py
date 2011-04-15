from nose.tools import *
from unittest import TestCase

from getting_better import GettingBetter

class GettingBetterTests(TestCase):
    def setUp(self):
        self.importer = MockImporter()
        self.gb = GettingBetter(importer=self.importer)
    
    def test_import_configfile_calls_load_source(self):
        self.gb.set_configfile('hello/there.py')
        self.gb.import_configfile()
        eq_('hello/there.py', self.importer.load_pathname)

class MockImporter(object):
    def __init__(self):
        self.load_name = None
        self.load_pathname = None
                
    def load_source(self, name, pathname):
        self.load_name = name
        self.load_pathname = pathname
        return None

