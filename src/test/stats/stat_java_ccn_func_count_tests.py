from nose.tools import *
from unittest import TestCase

from shutil import rmtree
from tempfile import mkdtemp

from stats.stat_java_ccn_func_count import StatJavaCcnFuncCount
from files.file_iterator import FileIterator
from files.file_package import FilePackage
from ccn_file_creator import CcnFileCreator

class StatJavaMeanCcnTests(TestCase):
    def setUp(self):
        self.ccn_file_creator = CcnFileCreator()

    def test_zero_ccn_func_count_when_limit_not_met(self):
        directory = mkdtemp("-caboose-java-ccn-count-low-single-test")
        self.ccn_file_creator.create_file_with_ccn(1, directory)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])
        
        stat = StatJavaCcnFuncCount()
        stat.set_ccn_limit(2)
        stat.set_files(file_iterator.files())
        eq_(0, stat.get_stat())
        rmtree(directory)

    def test_ccn_func_count_when_over_limit_single(self):
        directory = mkdtemp("-caboose-java-ccn-count-high-single-test")
        self.ccn_file_creator.create_file_with_ccn(5, directory)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])
        
        stat = StatJavaCcnFuncCount()
        stat.set_ccn_limit(2)
        stat.set_files(file_iterator.files())
        eq_(1, stat.get_stat())
        rmtree(directory)

    def test_ccn_func_count_when_over_limit_multiple(self):
        directory = mkdtemp("-caboose-java-ccn-count-high-single-test")
        self.ccn_file_creator.create_file_with_funcs_with_ccns(directory, [5, 1, 3, 2])

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])
        
        stat = StatJavaCcnFuncCount()
        stat.set_ccn_limit(3)
        stat.set_files(file_iterator.files())
        eq_(2, stat.get_stat())
        rmtree(directory)

    def test_stat_has_right_name(self):
        eq_(StatJavaCcnFuncCount.get_name(), "java_ccn_func_count")
