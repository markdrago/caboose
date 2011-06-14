import nose
from nose.tools import *
from unittest import TestCase

from os import path
from shutil import rmtree
from uuid import uuid4
from tempfile import mkdtemp

from stats.stat_java_ncss import StatJavaNcss
from files.file_iterator import FileIterator
from files.file_package import FilePackage

class StatLinesTests(TestCase):
    def test_proper_number_of_lines_are_counted_in_single_file(self):
        directory = mkdtemp("-caboose-java-ncss-single-test")
        self._create_file_with_lines(directory, 2, 4, 2)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatJavaNcss()
        stat.set_files(file_iterator.files())
        eq_(2, stat.get_stat())
        rmtree(directory)

    def test_proper_number_of_lines_are_counted_in_multiple_files(self):
        directory = mkdtemp("-caboose-numlines-multiple-test")
        self._create_file_with_lines(directory, 2, 4, 2)
        self._create_file_with_lines(directory, 8, 3, 11)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatJavaNcss()
        stat.set_files(file_iterator.files())
        eq_(10, stat.get_stat())
        rmtree(directory)
    
    def test_proper_number_of_lines_are_counted_in_inner_dir(self):
        directory = mkdtemp("-caboose-numlines-inner-dir-test")
        inner = mkdtemp("-inner-dir", dir=directory)
        self._create_file_with_lines(directory, 2, 3, 4)
        self._create_file_with_lines(inner, 5, 6, 7)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        stat = StatJavaNcss()
        stat.set_files(file_iterator.files())
        eq_(7, stat.get_stat())
        rmtree(directory)

    def test_proper_number_of_lines_in_multiple_dirs(self):
        directory = mkdtemp("-caboose-numlines-multiple-dir-test")
        inner1 = mkdtemp("-inner-dir1", dir=directory)
        inner2 = mkdtemp("-inner-dir2", dir=directory)
        inner3 = mkdtemp("-inner-dir3", dir=directory)
        self._create_file_with_lines(directory, 2, 3, 4)
        self._create_file_with_lines(inner1, 5, 6, 7)
        self._create_file_with_lines(inner2, 8, 9 ,10)
        self._create_file_with_lines(inner3, 13, 14, 15)

        fp = FilePackage()
        fp.add_directories(inner1, inner3)
        file_iterator = FileIterator([fp])

        stat = StatJavaNcss()
        stat.set_files(file_iterator.files())
        eq_(18, stat.get_stat())
        rmtree(directory)

    def test_stat_lines_counts_zero_if_directory_does_not_exist(self):
        directory = mkdtemp("-caboose-non-exist-dir-test")
        inner = path.join(directory, 'nonexistant')

        fp = FilePackage()
        fp.add_directory(inner)
        file_iterator = FileIterator([fp])

        stat = StatJavaNcss()
        stat.set_files(file_iterator.files())
        eq_(0, stat.get_stat())
        rmtree(directory)
    
    #this test used to cause an OSError: Argument list too long
    def test_stat_lines_works_with_absurd_number_of_files(self):
        directory = mkdtemp("-caboose-absurd-file-count-test")
        self._create_file_with_lines(directory, 5, 6, 7)

        fp = FilePackage()
        fp.add_directory(directory)
        file_iterator = FileIterator([fp])

        files = file_iterator.files()

        #count the same file 5000 times
        files = files * 5000

        stat = StatJavaNcss()
        stat._set_ncss_command("bash -c 'for x in `seq $#`; do echo 5; done' filler")
        stat.set_files(files)
        eq_(25000, stat.get_stat())
        rmtree(directory)
    
    def test_stat_has_right_name(self):
        stat = StatJavaNcss()
        eq_(stat.get_name(), "java_ncss")
    
    @nottest
    def _create_file_with_lines(self, directory, source_lines, non_source_lines, blank_lines, suffix=".java"):
        filename = path.join(directory, "%s%s" % (str(uuid4()), suffix))

        first_line = True
        close_class = False
        with open(filename, "w") as f:

            for i in range(max(source_lines, non_source_lines, blank_lines)):

                if non_source_lines > 0:
                    f.write("//comment goes here #%d\n" % i)
                    non_source_lines -= 1

                if source_lines > 0:
                    if first_line:
                        f.write("public class testClass {\n")
                        first_line = False
                        close_class = True
                    else:
                        f.write("int x = %d;\n" % i)
                    source_lines -= 1

                if blank_lines > 0:
                    f.write("\n")
                    blank_lines -= 1

            if close_class:
                f.write("}\n")
            f.close()

