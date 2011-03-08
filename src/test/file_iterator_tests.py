import nose
from nose.tools import *
from unittest import TestCase

import os
from shutil import rmtree
from tempfile import mkdtemp

from file_iterator import FileIterator

class FileIteratorTests(TestCase):
    def setUp(self):
        self.directory = mkdtemp('-gb-file-iterator-tests')
        self.file_iterator = FileIterator([self.directory])

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
    
    def test_match_files_by_glob(self):
        self.file_iterator.set_glob("*.java")
        self._create_file(self.directory, 'file.txt')
        self._create_file(self.directory, 'file.java')
        s = set(self.file_iterator.files())
        eq_(set([os.path.join(self.directory, 'file.java')]), s)

    def test_match_files_in_directory_tree_by_glob(self):
        self.file_iterator.set_glob("*.java")
        self._create_file(self.directory, 'file0.java')
        dir1 = self._create_dir(self.directory, 'dir1')
        self._create_file(dir1, 'file1.c')
        dir2 = self._create_dir(dir1, 'dir2')
        self._create_file(dir2, 'file2.java')
        dir3 = self._create_dir(self.directory, 'dir3')
        self._create_file(dir3, 'file3.py')
        
        expected = set()
        expected.add(os.path.join(self.directory, 'file0.java'))
        expected.add(os.path.join(dir2, 'file2.java'))
        s = set(self.file_iterator.files())
        eq_(expected, s)

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

