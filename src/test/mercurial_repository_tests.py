import nose
from nose.tools import *
from unittest import TestCase
from shutil import rmtree

from mercurial import commands

from mercurial_repository import MercurialRepository

from test_utils import hg_test_utils

class MercurialRepositoryTests(TestCase):
    def setUp(self):
        (self.repo, self.directory, self.hg_ui) = hg_test_utils.create_repo()
        self.hgs = MercurialRepository()

    def tearDown(self):
        rmtree(self.directory)
        
    def test_switch_to_revision(self):
        hg_test_utils.create_changesets(self.repo, 3)
        self.hgs.switch_to_revision(1, self.directory)
        repo = hg_test_utils.get_repo_for_directory(self.directory)
        eq_(1, hg_test_utils.get_working_directory_parent_revision(repo))
    
    def test_switch_to_date(self):
        dates = ('2011-01-01', '2011-02-02', '2011-03-03')
        hg_test_utils.create_changesets(self.repo, 3, dates=dates)
        self.hgs.switch_to_date('2011-02-02', self.directory)
        repo = hg_test_utils.get_repo_for_directory(self.directory)
        eq_(1, hg_test_utils.get_working_directory_parent_revision(repo))

