import nose
from nose.tools import *
from unittest import TestCase

from shutil import rmtree

from lib import hg
from mercurial import commands

from . import *

class HgSwitcherTests(TestCase):
    def setUp(self):
        (self.repo, self.directory, self.hg_ui) = hg.create_repo()
        hg.create_changesets(self.repo, 3)
        self.hgs = HgSwitcher()

    def tearDown(self):
        rmtree(self.directory)
        
    def test_switch_to_revision(self):
        assert_not_equal(1, hg.get_working_directory_parent_revision(self.repo))
        self.hgs.switch_to_revision(1, self.directory)
        repo = hg.get_repo_for_directory(self.directory)
        eq_(1, hg.get_working_directory_parent_revision(repo))

