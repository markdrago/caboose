from nose.tools import *
from unittest import TestCase

import os
from shutil import rmtree
from tempfile import mkdtemp

from files.file_package import FilePackage

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

    def test_file_package_add_basedir_subdirs(self):
        basedir = mkdtemp('-caboose-file-iterator-tests')

        expected_dirs = set()
        for subdir in ("dir1", "dir2", "dir3"):
            newdir = os.path.join(basedir, subdir)
            os.mkdir(newdir)
            expected_dirs.add(newdir)

        #add a file which should be ignored as it is not a directory
        filepath = os.path.join(basedir, "file1")
        with open(filepath, 'w') as f:
            f.write("file contents here")

        fp = FilePackage()
        fp.set_basedir(basedir)
        fp.add_basedir_subdirectories()

        eq_(expected_dirs, set(fp.get_directories()))

        rmtree(basedir)

class MockFileMatcher(object):
    def match(self):
        return True

