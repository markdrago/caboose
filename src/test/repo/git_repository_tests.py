from nose.tools import *
from unittest import TestCase
import repo_test_utils

import os
from shutil import rmtree
from tempfile import mkdtemp

from repo.git_repository import GitRepository
from repo.git_repository import GitRepositoryException

class GitRepositoryTests(TestCase):
    def setUp(self):
        self.directory = mkdtemp('-caboose-git-repo-tests')
        self.rmtree = False

    def tearDown(self):
        if self.rmtree:
            rmtree(self.directory)

    @raises(GitRepositoryException)
    def test_init_raises_with_non_git_directory(self):
        gitrepo = GitRepository(self.directory)

    def test_init_creates_repo_when_init_set_to_true(self):
        ok_(not os.path.isdir(os.path.join(self.directory, '.git')))
        gitrepo = GitRepository(self.directory, init=True)
        ok_(os.path.isdir(os.path.join(self.directory, '.git')))

    def test_adding_a_file_adds_it_to_the_git_index(self):
        gitrepo = GitRepository(self.directory, init=True)
        filename = repo_test_utils._create_random_file(self.directory)
        gitrepo.add(filename)
        result = gitrepo.run_git("status --porcelain")
        eq_("A  %s\n" % (os.path.basename(filename),), result)

    @nottest
    def test_get_date_of_earliest_commit(self):
        gitrepo = GitRepository(self.directory)
        #TODO: make a few commits, setting the dates
        date = gitrepo.get_date_of_earliest_commit()
        #make sure date matches expected date

    @nottest
    def create_test_changesets(self, repo, count=1, dates=[]):
        for i in range(count):
            filename = repo_test_utils._create_random_file(self.directory)
            commands.add(repo.get_ui(), repo.get_repo(), filename)
            
            date=None
            if i < len(dates):
                date=dates[i]
            commands.commit(repo.get_ui(), repo.get_repo(), date=date, message="creating test commit", user='Test Runner <trunner@domain.com>')

