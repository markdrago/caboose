import nose
from nose.tools import *
from unittest import TestCase

import os
from shutil import rmtree
from tempfile import mkdtemp
from uuid import uuid4
from mercurial import commands

from mercurial_repository import MercurialRepository

class MercurialRepositoryTests(TestCase):
    def setUp(self):
        self.directory = mkdtemp('-gbtests')
    
    def tearDown(self):
        rmtree(self.directory)

    @raises(Exception)
    def test_init_raises_with_init_false_and_non_hg_directory(self):
        hgrepo = MercurialRepository(self.directory, init=False)
        
    def test_init_creates_repo_with_init_true_and_non_hg_directory(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        ok_(os.path.isdir(os.path.join(self.directory, '.hg')))

    def test_switch_to_revision(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        self.create_test_changesets(hgrepo, 3)
        hgrepo.switch_to_revision(1)
        eq_(1, hgrepo.get_working_directory_parent_revision())
    
    def test_switch_to_date(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        dates = ('2011-01-01', '2011-02-02', '2011-03-03')
        self.create_test_changesets(hgrepo, 3, dates=dates)
        hgrepo.switch_to_date('2011-02-02')
        eq_(1, hgrepo.get_working_directory_parent_revision())

    @nottest
    def create_test_changesets(self, repo, count=1, dates=[]):
        for i in range(count):
            filename = self._create_random_file()
            commands.add(repo.get_ui(), repo.get_repo(), filename)
            
            date=None
            if i < len(dates):
                date=dates[i]
            commands.commit(repo.get_ui(), repo.get_repo(), date=date, message="creating %s" % (filename,))
    
    @nottest        
    def _create_random_file(self):
        filename = os.path.join(self.directory, str(uuid4()))
        with open(filename, 'w') as f:
            f.write(filename)
            f.close()
        return filename

