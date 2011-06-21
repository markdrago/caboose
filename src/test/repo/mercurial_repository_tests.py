import nose
from nose.tools import *
from unittest import TestCase

import os
from shutil import rmtree
from tempfile import mkdtemp
from datetime import datetime
from mercurial import commands

from repo.mercurial_repository import MercurialRepository

class MercurialRepositoryTests(TestCase):
    def setUp(self):
        self.directory = mkdtemp('-caboose-hg-repo-tests')
    
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
        dates = ('2011-01-01', '2011-02-02', '2011-03-03')
        self.create_test_changesets(hgrepo, 3, dates=dates)
        hgrepo.switch_to_revision(1)
        eq_('37852bd42d8ae89ea30c2ce2c429459ac83303bd', hgrepo.get_working_directory_parent_revision())
    
    def test_switch_to_date(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        dates = ('2011-01-01', '2011-02-02', '2011-03-03')
        self.create_test_changesets(hgrepo, 3, dates=dates)
        hgrepo.switch_to_date(datetime(2011, 2, 2))
        eq_('37852bd42d8ae89ea30c2ce2c429459ac83303bd', hgrepo.get_working_directory_parent_revision())

    def test_switch_to_commit_before_date_time(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        dates = ('2011-01-01 01:01:01', '2011-02-02 02:02:02', '2011-03-03 03:03:03')
        self.create_test_changesets(hgrepo, 3, dates=dates)
        hgrepo.switch_to_before_date(datetime(2011, 2, 2, 4, 4, 4))
        eq_('9699b017dc594de1d07ebc994e63aeddf31da8b8', hgrepo.get_working_directory_parent_revision())
    
    def test_get_revision_before_date_time(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        dates = ('2011-01-01 01:01:01', '2011-02-02 02:02:02', '2011-03-03 03:03:03')
        self.create_test_changesets(hgrepo, 3, dates=dates)
        eq_('9699b017dc594de1d07ebc994e63aeddf31da8b8', hgrepo.get_revision_before_date(datetime(2011, 2, 2, 4, 4, 4)))

    def test_get_revision_before_date_time_stays_on_branch(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        dates = ('2011-01-01 01:01:01', '2011-03-03 03:03:03')
        self.create_test_changesets(hgrepo, 2, dates=dates)

        hgrepo.create_and_switch_to_branch('avoidbranch')
        self.create_test_changesets(hgrepo, 1, dates=('2011-02-02 02:02:02',))

        commands.update(hgrepo.get_ui(), hgrepo.get_repo(), rev='default')

        #should match commit on 2011-01-01, not 2011-02-02
        eq_('f957b16de26a4879c255762cee97797a64e28f28', hgrepo.get_revision_before_date(datetime(2011, 2, 2, 4, 4, 4)))

    def test_create_and_switch_to_branch(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        hgrepo.create_and_switch_to_branch('newbranch')
        eq_('newbranch', hgrepo.get_repo()[None].branch())

    def test_get_date_of_earliest_commit(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        dates = ('2011-01-01 01:01:01', '2011-02-02 02:02:02', '2011-03-03 03:03:03')
        self.create_test_changesets(hgrepo, 3, dates=dates)
        d = hgrepo.get_date_of_earliest_commit()
        eq_(datetime(2011, 1, 1, 1, 1, 1), d)

    def test_get_base_directory(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        d = hgrepo.get_base_directory()
        eq_(self.directory, d)
    
    def test_repo_uses_quiet_ui(self):
        hgrepo = MercurialRepository(self.directory, init=True)
        eq_(True, hgrepo.ui.quiet)

    @nottest
    def create_test_changesets(self, repo, count=1, dates=[]):
        for i in range(count):
            filename = self._create_random_file()
            commands.add(repo.get_ui(), repo.get_repo(), filename)
            
            date=None
            if i < len(dates):
                date=dates[i]
            commands.commit(repo.get_ui(), repo.get_repo(), date=date, message="creating test commit", user='Test Runner <trunner@domain.com>')
    
    @nottest        
    def _create_random_file(self):
        i = 0
        while True:
            filename = "file%d" % i
            filepath = os.path.join(self.directory, filename)
            if os.path.exists(filepath):
                i += 1
                continue
            with open(filepath, 'w') as f:
                f.write(filename)
                f.close()
            return filepath

