import nose
from nose.tools import *
from unittest import TestCase

from os import path
from shutil import rmtree
from tempfile import mkdtemp

from stat_lines import StatLines

class StatLinesTests(TestCase):
    def test_proper_number_of_lines_are_counted_in_single_file(self):
        directory = mkdtemp("-gbtests")
        filename = path.join(directory, "2_lines.java")
        with open(filename, "w") as f:
            f.write("line1\nline2\n")
            f.close()
        stat = StatLines(directory)
        eq_(2, stat.get_stat())
        rmtree(directory)
