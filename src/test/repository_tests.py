import nose
from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp

from repository import Repository
from repository_factory import RepositoryFactory
from mercurial_repository import MercurialRepository

class RepositoryTests(TestCase):
    @raises(Exception)
    def test_repository_switch_to_before_date_throws():
        r = Repository()
        r.switch_to_before_date('2011-01-01')
    
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

