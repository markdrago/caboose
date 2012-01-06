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
        basedir = mkdtemp('-caboose-file-package-tests')

        expected_dirs = set(("dir1", "dir2", "dir3"))
        self.produce_fake_directories(basedir, expected_dirs)
        expected_dirs = [os.path.join(basedir, name) for name in expected_dirs]

        #add a file which should be ignored as it is not a directory
        filepath = os.path.join(basedir, "file1")
        with open(filepath, 'w') as f:
            f.write("file contents here")

        fp = FilePackage()
        fp.set_basedir(basedir)
        fp.add_directory("*")

        eq_(set(expected_dirs), set(fp.get_directories()))

        rmtree(basedir)

    def test_file_package_includes_globbed_directories(self):
        basedir = mkdtemp('-caboose-file-package-tests2')
        dirs = ("1dir", "2dir", "different")
        self.produce_fake_directories(basedir, dirs)

        #create a file package which uses a globbed directory name
        fp = FilePackage()
        fp.set_basedir(basedir)
        fp.add_directory("*dir")

        expected = [os.path.join(basedir, name) for name in ("1dir", "2dir")]
        eq_(set(expected), set(fp.get_directories()))

    def test_file_package_excludes_excluded_directories(self):
        fp = FilePackage()
        fp.add_directory("dir1")
        fp.add_directories("dir2", "dir3", "dir4", "dir5")
        fp.exclude_directory("dir3")
        fp.exclude_directories("dir4", "dir5")
        eq_(set(("dir1", "dir2")), set(fp.get_directories()))

    @nottest
    def produce_fake_directories(self, basedir, dirs):
        for subdir in dirs:
            newdir = os.path.join(basedir, subdir)
            os.mkdir(newdir)

class MockFileMatcher(object):
    def match(self):
        return True

