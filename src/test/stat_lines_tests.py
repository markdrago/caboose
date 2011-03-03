import nose
from nose.tools import *
from unittest import TestCase

from os import path
from shutil import rmtree
from uuid import uuid4
from tempfile import mkdtemp

from stat_lines import StatLines

class StatLinesTests(TestCase):
    def test_proper_number_of_lines_are_counted_in_single_file(self):
        directory = mkdtemp("-gb-numlines-single-test")
        self._create_file_with_n_lines(directory, 2)
        stat = StatLines(directory)
        eq_(2, stat.get_stat())
        rmtree(directory)

    def test_proper_number_of_lines_are_counted_in_multiple_files(self):
        directory = mkdtemp("-gb-numlines-multiple-test")
        self._create_file_with_n_lines(directory, 2)
        self._create_file_with_n_lines(directory, 3)
        stat = StatLines(directory)
        eq_(5, stat.get_stat())
        rmtree(directory)
    
    def test_proper_number_of_lines_are_counted_in_multiple_dirs(self):
        directory = mkdtemp("-gb-numlines-multiple-dir-test")
        inner = mkdtemp("-inner-dir", dir=directory)
        self._create_file_with_n_lines(directory, 2)
        self._create_file_with_n_lines(inner, 5)
        stat = StatLines(directory)
        eq_(7, stat.get_stat())
        rmtree(directory)

    def test_only_counts_java_files(self):
        directory = mkdtemp("-gb-numlines-java-files-test")
        self._create_file_with_n_lines(directory, 2, suffix='.notjava')
        self._create_file_with_n_lines(directory, 5)
        stat = StatLines(directory)
        eq_(5, stat.get_stat())
        rmtree(directory)
    
    @nottest
    def _create_file_with_n_lines(self, directory, count, suffix='.java'):
        filename = path.join(directory, "%s%s" % (str(uuid4()), suffix))
        with open(filename, "w") as f:
            for i in range(1, count+1):
                f.write("line %d\n" % i)
            f.close()

