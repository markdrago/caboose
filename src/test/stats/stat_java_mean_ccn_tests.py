import nose
from nose.tools import *
from unittest import TestCase

from os import path
from shutil import rmtree
from tempfile import mkdtemp

from stats.stat_java_mean_ccn import StatJavaMeanCcn
from files.file_iterator import FileIterator
from files.file_package import FilePackage
from ccn_file_creator import CcnFileCreator

class StatJavaMeanCcnTests(TestCase):
    def setUp(self):
        self.ccn_file_creator = CcnFileCreator()

    def test_proper_ccn_is_found_in_single_file(self):
        directory = mkdtemp("-gb-java-ccn-single-test")
        self.ccn_file_creator.create_file_with_ccn(3, directory)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])
        
        stat = StatJavaMeanCcn()
        stat.set_files(file_iterator.files())
        eq_(3, stat.get_stat())
        rmtree(directory)

    def test_proper_ccn_is_found_in_multiple_files(self):
        directory = mkdtemp("-gb-java-ccn-multiple-test")
        self.ccn_file_creator.create_file_with_ccn(2, directory)
        self.ccn_file_creator.create_file_with_ccn(8, directory)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatJavaMeanCcn()
        stat.set_files(file_iterator.files())
        eq_(5, stat.get_stat())
        rmtree(directory)

    def test_proper_ccn_is_found_in_multiple_files_float(self):
        directory = mkdtemp("-gb-java-ccn-multiple-float-test")
        self.ccn_file_creator.create_file_with_ccn(3, directory)
        self.ccn_file_creator.create_file_with_ccn(8, directory)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatJavaMeanCcn()
        stat.set_files(file_iterator.files())
        eq_(5.5, stat.get_stat())
        rmtree(directory)
    
    def test_stat_lines_counts_zero_if_directory_does_not_exist(self):
        directory = mkdtemp("-gb-ccn-non-exist-dir-test")
        inner = path.join(directory, 'nonexistant')

        fp = FilePackage()
        fp.add_directory(inner)
        file_iterator = FileIterator([fp])

        stat = StatJavaMeanCcn()
        stat.set_files(file_iterator.files())
        eq_(0, stat.get_stat())
        rmtree(directory)
    
    def test_stat_has_right_name(self):
        stat = StatJavaMeanCcn()
        eq_(stat.get_name(), "meanccn")
    


