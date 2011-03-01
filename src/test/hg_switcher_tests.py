import nose
from nose.tools import *
from unittest import TestCase

from shutil import rmtree

from lib import hg
from mercurial import commands

from repository import HgSwitcher

class HgSwitcherTests(TestCase):
    def setUp(self):
        (self.repo, self.directory, self.hg_ui) = hg.create_repo()
        self.hgs = HgSwitcher()

    def tearDown(self):
        rmtree(self.directory)
        
    def test_switch_to_revision(self):
        hg.create_changesets(self.repo, 3)
        self.hgs.switch_to_revision(1, self.directory)
        repo = hg.get_repo_for_directory(self.directory)
        eq_(1, hg.get_working_directory_parent_revision(repo))
    
    def test_switch_to_date(self):
        dates = ('2011-01-01', '2011-02-02', '2011-03-03')
        hg.create_changesets(self.repo, 3, dates=dates)
        self.hgs.switch_to_date('2011-02-02', self.directory)
        repo = hg.get_repo_for_directory(self.directory)
        eq_(1, hg.get_working_directory_parent_revision(repo))

