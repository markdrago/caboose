from nose.tools import *
from unittest import TestCase
import repo_test_utils

import os
from shutil import rmtree
from tempfile import mkdtemp
from datetime import datetime

from repo.git_repository import GitRepository, GitRepositoryException

class GitRepositoryTests(TestCase):
    def setUp(self):
        self.directory = mkdtemp('-caboose-git-repo-tests')
        self.rmtree = True

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
        status = gitrepo.run_git("status --porcelain")
        eq_("A  %s\n" % (os.path.basename(filename),), status)

    def test_commiting_actually_creates_a_new_commit(self):
        #create repo and add file
        gitrepo = GitRepository(self.directory, init=True)
        self.create_single_file_and_add_to_repository(gitrepo)

        #commit and verify commit was created
        gitrepo.commit(message='testmessage')
        message = gitrepo.run_git("log --format=%s")
        eq_("testmessage\n", message)

    def test_set_date_on_git_commit(self):
        gitrepo = GitRepository(self.directory, init=True)
        self.create_single_file_and_add_to_repository(gitrepo)
        
        expected_date = datetime(2011, 10, 28, 8, 0, 0)
        gitrepo.commit(message='testmessage', date=expected_date)
        actual_date = gitrepo.run_git("log --format=%cd --date=iso")
        actual_date = gitrepo.convert_git_date_to_datetime(actual_date)
        eq_(expected_date, actual_date)

    def test_convert_git_date_to_datetime(self):
        gitrepo = GitRepository(self.directory, init=True)
        gitdate = '2011-10-23 17:35:20 -0400'
        dt = gitrepo.convert_git_date_to_datetime(gitdate)
        eq_(datetime(2011, 10, 23, 17, 35, 20), dt)

    def test_get_date_of_earliest_commit(self):
        #create repo and add file
        gitrepo = GitRepository(self.directory, init=True)
        expected_date = datetime(2011, 10, 28, 8, 4, 0)
        self.create_single_file_add_and_commit_it(gitrepo, date=expected_date)
        
        #make a few more commits
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 5, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 6, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 7, 0))
        
        #make sure when we ask for the earliest date, we get the first one
        earliest = gitrepo.get_date_of_earliest_commit()
        eq_(expected_date, earliest)

    def test_get_revision_before_date(self):
        #create repo
        gitrepo = GitRepository(self.directory, init=True)
        
        #make a few commits
        date_of_target_commit = datetime(2011, 10, 28, 8, 5, 0)
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 4, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=date_of_target_commit)
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 6, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 7, 0))

        #get sha1 of target commit (since we know it is the second commit)
        target_sha1 = gitrepo.run_git("log --format=%H --skip=2 -1")
        target_sha1 = target_sha1.strip()

        #make sure when we ask for sha1 of the commit before a date we get the right one
        actual_sha1 = gitrepo.get_revision_before_date(datetime(2011, 10, 28, 8, 5, 45))
        eq_(target_sha1, actual_sha1)

    def test_get_revision_before_date_stays_on_current_branch(self):
        #create repo
        gitrepo = GitRepository(self.directory, init=True)
        
        #make a few commits
        date_of_target_commit = datetime(2011, 10, 28, 8, 5, 0)
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 4, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=date_of_target_commit)
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 6, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 7, 0))

        #get sha1 of target commit (since we know it is the second commit)
        target_sha1 = gitrepo.run_git("log --format=%H --skip=2 -1")
        target_sha1 = target_sha1.strip()
        
        #create a new branch and commits on it, with one commit that would be
        #a better match for the requested date, except it is on a different branch
        gitrepo.create_branch("newbranch")
        gitrepo.switch_to_revision("newbranch")
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 4, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 5, 30))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 10, 28, 8, 6, 0))

        #make sure when we ask for sha1 of the commit before a date we get the right one
        gitrepo.switch_to_revision("master")
        actual_sha1 = gitrepo.get_revision_before_date(datetime(2011, 10, 28, 8, 5, 45))
        eq_(target_sha1, actual_sha1)

    def test_get_revision_before_date_can_find_commits_later_than_current_working_directory(self):
        #create repo
        gitrepo = GitRepository(self.directory, init=True)
        
        #make a few commits
        target_date = datetime(2011, 11, 1, 20, 38, 0)
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 11, 1, 20, 35, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 11, 1, 20, 36, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 11, 1, 20, 37, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=target_date)

        #get sha1 of an early and a late commit
        early_sha1 = gitrepo.run_git("log --format=%H --skip=2 -1").strip()
        late_sha1 = gitrepo.run_git("log --format=%H -1").strip()
       
        #switch to early_sha1
        gitrepo.switch_to_revision(early_sha1)
        
        #make sure when we ask for sha1 of the commit before a date we get the right one
        actual_sha1 = gitrepo.get_revision_before_date(datetime(2011, 11, 1, 20, 38, 30))
        eq_(late_sha1, actual_sha1)

    def test_switch_to_revision(self):
        #create repo
        gitrepo = GitRepository(self.directory, init=True)
        
        #make a few commits
        date_of_target_commit = datetime(2011, 11, 1, 7, 25, 0)
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 11, 1, 7, 24, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=date_of_target_commit)
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 11, 1, 7, 26, 0))
        self.create_single_file_add_and_commit_it(gitrepo, date=datetime(2011, 11, 1, 7, 27, 0))

        #get sha1 of target commit (since we know it is the second commit)
        target_sha1 = gitrepo.run_git("log --format=%H --skip=2 -1")
        target_sha1 = target_sha1.strip()
        
        #switch to target commit
        gitrepo.switch_to_revision(target_sha1)
        
        #make sure we are on the target commit
        result = gitrepo.run_git("rev-parse HEAD").strip()
        eq_(target_sha1, result)

    def test_get_base_directory(self):
        gitrepo = GitRepository(self.directory, init=True)
        eq_(self.directory, gitrepo.get_base_directory())

    @nottest
    def create_single_file_add_and_commit_it(self, gitrepo, date=None):
        self.create_single_file_and_add_to_repository(gitrepo)
        gitrepo.commit(message='testmessage', date=date)

    @nottest
    def create_single_file_and_add_to_repository(self, gitrepo):
        filename = repo_test_utils._create_random_file(self.directory)
        gitrepo.add(filename)

        #verify the file is not committed
        status = gitrepo.run_git("status --porcelain")
        eq_("A  %s\n" % (os.path.basename(filename),), status)

    @nottest
    def create_test_changesets(self, repo, count=1, dates=[]):
        for i in range(count):
            filename = repo_test_utils._create_random_file(self.directory)
            commands.add(repo.get_ui(), repo.get_repo(), filename)
            
            date=None
            if i < len(dates):
                date=dates[i]
            commands.commit(repo.get_ui(), repo.get_repo(), date=date, message="creating test commit", user='Test Runner <trunner@domain.com>')

