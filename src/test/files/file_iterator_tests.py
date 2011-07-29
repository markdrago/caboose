from nose.tools import *
from unittest import TestCase

import os
from shutil import rmtree
from tempfile import mkdtemp

from files.file_iterator import FileIterator
from files.file_package import FilePackage

class FileIteratorTests(TestCase):
    def setUp(self):
        self.directory = mkdtemp('-caboose-file-iterator-tests')
        self.file_package = FilePackage()
        self.file_package.add_directory(self.directory)
        self.file_iterator = FileIterator([self.file_package,])

    def tearDown(self):
        rmtree(self.directory)

    def test_iterate_files_in_single_directory(self):
        self._create_file(self.directory, 'file1')
        self._create_file(self.directory, 'file2')
        s = set(self.file_iterator.files())
        eq_(set(self._prepend_dir(['file1', 'file2'])), s)
    
    def test_iterate_files_in_directory_tree(self):
        self._create_file(self.directory, 'file0')
        dir1 = self._create_dir(self.directory, 'dir1')
        self._create_file(dir1, 'file1')
        dir2 = self._create_dir(dir1, 'dir2')
        self._create_file(dir2, 'file2')
        dir3 = self._create_dir(self.directory, 'dir3')
        self._create_file(dir3, 'file3')
        
        expected = set()
        expected.add(os.path.join(self.directory, 'file0'))
        expected.add(os.path.join(dir1, 'file1'))
        expected.add(os.path.join(dir2, 'file2'))
        expected.add(os.path.join(dir3, 'file3'))
        s = set(self.file_iterator.files())
        eq_(expected, s)
    
    def test_match_files_by_filematcher(self):
        self._create_file(self.directory, 'file.txt')
        self._create_file(self.directory, 'file.java')
  
        fm = MockFileMatcher()
        fm.add_match("file.java")
        fp = FilePackage()
        fp.add_directory(self.directory)
        fp.add_file_matcher(fm)
        self.file_iterator.set_filepackages([fp])
  
        s = set(self.file_iterator.files())
        eq_(set([os.path.join(self.directory, 'file.java')]), s)

    def test_match_files_in_directory_tree_by_filematcher(self):
        self._create_file(self.directory, 'file0.java')
        dir1 = self._create_dir(self.directory, 'dir1')
        self._create_file(dir1, 'file1.c')
        dir2 = self._create_dir(dir1, 'dir2')
        self._create_file(dir2, 'file2.java')
        dir3 = self._create_dir(self.directory, 'dir3')
        self._create_file(dir3, 'file3.py')

        fm = MockFileMatcher()
        fm.add_match("file0.java")
        fm.add_match("file2.java")
        fp = FilePackage()
        fp.add_directory(self.directory)
        fp.add_file_matcher(fm)
        self.file_iterator.set_filepackages([fp])
        
        expected = set()
        expected.add(os.path.join(self.directory, 'file0.java'))
        expected.add(os.path.join(dir2, 'file2.java'))
        s = set(self.file_iterator.files())
        eq_(expected, s)

    def test_iterate_files_in_multiple_directories(self):
        dir1 = self._create_dir(self.directory, 'dir1')
        dir2 = self._create_dir(self.directory, 'dir2')
        self._create_file(dir1, 'file1')
        self._create_file(dir2, 'file2')
        fp = FilePackage()
        fp.add_directories(dir1, dir2)
        self.file_iterator.set_filepackages([fp])
        expected = set()
        expected.add(os.path.join(dir1, 'file1'))
        expected.add(os.path.join(dir2, 'file2'))
        s = set(self.file_iterator.files())
        eq_(expected, s)
    
    def test_file_iterator_gets_stats_for_dir_relative_to_base_dir(self):
        dir1full = self._create_dir(self.directory, 'dir1')
        self._create_file(dir1full, 'file1')
        self._create_file(dir1full, 'file2')
        fp = FilePackage()
        fp.add_directory("dir1")
        fp.set_basedir(self.directory)
        self.file_iterator.set_filepackages([fp])
        s = set(self.file_iterator.files())
        eq_(set(self._prepend_dir(['file1', 'file2'], dir1full)), s)

    def test_file_iterator_acts_like_iterator(self):
        files = ['file.txt', 'file.java']
        need_to_find = [os.path.join(self.directory, f) for f in files]
        
        for f in need_to_find:
            self._create_file(self.directory, f)
        for f in self.file_iterator:
            need_to_find.remove(f)
        eq_(0, len(need_to_find))

    def test_file_iterator_excludes_broken_symlinks(self):
        files = ['exists.txt', 'movealong.txt']

        self._create_file(self.directory, 'exists.txt')
        os.symlink(os.path.join(self.directory, 'movealong.txt'),
                   os.path.join(self.directory, 'broken.txt'))

        eq_(1, len(self.file_iterator.files()))
        eq_(os.path.join(self.directory, 'exists.txt'), self.file_iterator.files()[0])

    def test_file_iterator_excludes_excluded_path_globs(self):
        srcdir = self._create_dir(self.directory, 'src')
        self._create_file(srcdir, 'srcfile.java')
        testdir = self._create_dir(self.directory, 'test')
        self._create_file(testdir, 'testfile.java')

        self.file_iterator.exclude_path_globs(*["*/test/*"])

        eq_(1, len(self.file_iterator.files()))
        eq_(os.path.join(srcdir, 'srcfile.java'), self.file_iterator.files()[0])

    @nottest
    def _create_file(self, directory, filename):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as f:
            f.write(filename)
            f.close()

    @nottest
    def _create_dir(self, directory, dirname):
        dirpath = os.path.join(directory, dirname)
        os.mkdir(dirpath)
        return dirpath

    @nottest
    def _prepend_dir(self, files, directory=None):
        if directory is None:
            directory = self.directory
        return [os.path.join(directory, f) for f in files]

class MockFileMatcher(object):
    def __init__(self):
        self.matches = []
    
    def add_match(self, filename):
        self.matches.append(filename)
    
    def match(self, filename):
        return (filename in self.matches)

