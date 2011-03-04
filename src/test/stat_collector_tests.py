import nose
from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp
from mercurial import commands

from mercurial_repository import MercurialRepository

#class StatCollectorTests(TestCase):
#    def test_stat_collector_gathers_single_simple_stat(self):
#        directory = mkdtemp('-gb-stat-collector-tests')
#        hgrepo = MercurialRepository(directory, init=True)
#        sc = StatCollector(hgrepo, directory, SimpleStat)
        
class SimpleStat(object):
    def __init__(self, directory):
        pass
    
    def get_stat(self):
        return 1

