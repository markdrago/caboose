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
        self.file_iterator = FileIterator(self.directory)

    def tearDown(self):
        rmtree(self.directory)

    def test_iterate_files_in_single_directory(self):
        self._create_file(self.directory, 'file1')
        self._create_file(self.directory, 'file2')
        l = list(self.file_iterator.files())
        eq_(self._prepend_dir(['file1', 'file2']), l)

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

