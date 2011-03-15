from nose.tools import *
from unittest import TestCase

import os
from shutil import rmtree
from tempfile import mkdtemp

from file_package import FilePackage

class FilePackageTests(TestCase):
    def test_file_package_holds_directories(self):
        fp = FilePackage()
        fp.add_directory("dir1")
        eq_(set(("dir1",)), set(fp.get_directories()))

    def test_file_package_holds_many_directories(self):
        fp = FilePackage()
        fp.add_directory("dir1")
        fp.add_directories("dir2", "dir3")
        eq_(set(("dir1", "dir2", "dir3")), set(fp.get_directories()))

    def test_file_package_holds_file_matchers(self):
        fp = FilePackage()
        fm = MockFileMatcher()
        fp.add_file_matcher(fm)
        eq_(set((fm,)), set(fp.get_file_matchers()))

    def test_file_package_holds_many_file_matchers(self):
        fp = FilePackage()
        fm1 = MockFileMatcher()
        fm2 = MockFileMatcher()
        fp.add_file_matchers(fm1, fm2)
        eq_(set((fm1, fm2)), set(fp.get_file_matchers()))

    def test_file_package_prepends_basedir(self):
        fp = FilePackage()
        fp.set_basedir("/tmp/basedirname")
        fp.add_directories("dir1", "dir2")
        expected = set(("/tmp/basedirname/dir1", "/tmp/basedirname/dir2"))
        eq_(expected, set(fp.get_directories()))

class MockFileMatcher(object):
    def match(self):
        return True

