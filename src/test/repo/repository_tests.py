import nose
from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp

from repo.repository_factory import RepositoryFactory
from repo.mercurial_repository import MercurialRepository

class RepositoryTests(TestCase):
    @raises(Exception)
    def test_repository_get_revision_before_date_throws(self):
        r = Repository()
        r.get_revision_before_date('2011-01-01')
    
    @raises(Exception)
    def test_repository_get_date_of_earliest_commit_throws(self):
        r = Repository()
        r.get_date_of_earliest_commit()
    
    @raises(Exception)
    def test_repository_switch_to_revision_throws(self):
        r = Repository()
        r.switch_to_revision(0)
        
    @raises(Exception)
    def test_repository_get_base_directory_throws(self):
        r = Repository()
        r.get_base_directory()
    
    def test_get_mercurial_repo_from_factory_for_directory_with_hg_repo(self):
        directory = mkdtemp('-gb-rep-works-test')
        MercurialRepository(directory, init=True)
        repo = RepositoryFactory.get_repository(directory)
        eq_(MercurialRepository, type(repo))
        rmtree(directory)

    @raises(Exception)
    def test_repository_factory_throws_for_directory_without_repo(self):
        directory = mkdtemp('-gb-rep-fails-correctly-test')
        try:
            repo = RepositoryFactory.get_repository(directory)
        finally:
            rmtree(directory)

