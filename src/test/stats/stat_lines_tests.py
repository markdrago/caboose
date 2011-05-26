import nose
from nose.tools import *
from unittest import TestCase

from os import path
from shutil import rmtree
from uuid import uuid4
from tempfile import mkdtemp

from stats.stat_lines import StatLines
from files.file_iterator import FileIterator
from files.file_package import FilePackage

class StatLinesTests(TestCase):
    def test_proper_number_of_lines_are_counted_in_single_file(self):
        directory = mkdtemp("-gb-numlines-single-test")
        self._create_file_with_n_lines(directory, 2)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatLines()
        stat.set_files(file_iterator.files())
        eq_(2, stat.get_stat())
        rmtree(directory)

    def test_proper_number_of_lines_are_counted_in_multiple_files(self):
        directory = mkdtemp("-gb-numlines-multiple-test")
        self._create_file_with_n_lines(directory, 2)
        self._create_file_with_n_lines(directory, 3)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatLines()
        stat.set_files(file_iterator.files())
        eq_(5, stat.get_stat())
        rmtree(directory)
    
    def test_proper_number_of_lines_are_counted_in_inner_dir(self):
        directory = mkdtemp("-gb-numlines-inner-dir-test")
        inner = mkdtemp("-inner-dir", dir=directory)
        self._create_file_with_n_lines(directory, 2)
        self._create_file_with_n_lines(inner, 5)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatLines()
        stat.set_files(file_iterator.files())
        eq_(7, stat.get_stat())
        rmtree(directory)

    def test_proper_number_of_lines_in_multiple_dirs(self):
        directory = mkdtemp("-gb-numlines-multiple-dir-test")
        inner1 = mkdtemp("-inner-dir1", dir=directory)
        inner2 = mkdtemp("-inner-dir2", dir=directory)
        inner3 = mkdtemp("-inner-dir3", dir=directory)
        self._create_file_with_n_lines(directory, 2)
        self._create_file_with_n_lines(inner1, 5)
        self._create_file_with_n_lines(inner2, 8)
        self._create_file_with_n_lines(inner3, 13)

        fp = FilePackage()
        fp.add_directories(inner1, inner3)
        file_iterator = FileIterator([fp])

        stat = StatLines()
        stat.set_files(file_iterator.files())
        eq_(18, stat.get_stat())
        rmtree(directory)

    def test_stat_lines_counts_zero_if_directory_does_not_exist(self):
        directory = mkdtemp("-gb-non-exist-dir-test")
        inner = path.join(directory, 'nonexistant')

        fp = FilePackage()
        fp.add_directory(inner)
        file_iterator = FileIterator([fp])

        stat = StatLines()
        stat.set_files(file_iterator.files())
        eq_(0, stat.get_stat())
        rmtree(directory)

    def test_stat_has_right_name(self):
        stat = StatLines()
        eq_(stat.get_name(), "lines")
    
    @nottest
    def _create_file_with_n_lines(self, directory, count, suffix='.java'):
        filename = path.join(directory, "%s%s" % (str(uuid4()), suffix))
        with open(filename, "w") as f:
            for i in range(1, count+1):
                f.write("line %d\n" % i)
            f.close()
