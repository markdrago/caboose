import nose
from nose.tools import *
from unittest import TestCase

from os import path
from shutil import rmtree
from uuid import uuid4
from tempfile import mkdtemp

from stat_java_mean_ccn import StatJavaMeanCcn
from file_iterator import FileIterator
from file_package import FilePackage

class StatJavaMeanCcnTests(TestCase):
    def test_proper_ccn_is_found_in_single_file(self):
        directory = mkdtemp("-gb-java-ccn-single-test")
        self._create_file_with_ccn(directory, 3)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])
        
        stat = StatJavaMeanCcn()
        stat.set_files(file_iterator.files())
        eq_(3, stat.get_stat())
        rmtree(directory)

    def test_proper_ccn_is_found_in_multiple_files(self):
        directory = mkdtemp("-gb-java-ccn-multiple-test")
        self._create_file_with_ccn(directory, 2)
        self._create_file_with_ccn(directory, 8)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatJavaMeanCcn()
        stat.set_files(file_iterator.files())
        eq_(5, stat.get_stat())
        rmtree(directory)

    def test_proper_ccn_is_found_in_multiple_files_float(self):
        directory = mkdtemp("-gb-java-ccn-multiple-float-test")
        self._create_file_with_ccn(directory, 3)
        self._create_file_with_ccn(directory, 8)

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
    
    @nottest
    def _create_file_with_ccn(self, directory, ccn, suffix=".java"):
        filename = path.join(directory, "%s%s" % (str(uuid4()), suffix))

        with open(filename, "w") as f:
            f.write("public class testClass {\n\n")
            f.write("  public void testFunc() {\n")
            f.write("    int x = 1;\n\n")
            for i in range(ccn - 1):
                line = "    if (x == %d) { System.out.println(\"x is %d\"); }\n\n"
                f.write(line % (i, i))
            f.write("  }\n")
            f.write("}\n")
            f.close()

