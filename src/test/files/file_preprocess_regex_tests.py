from nose.tools import *
from unittest import TestCase

import re   

from files.file_preprocess_regex import FilePreProcessRegex

class FilePreProcessRegexTests(TestCase):
    def setUp(self):
        self.ppr = FilePreProcessRegex()
    
    def test_simple_matcher(self):
        self.ppr.set_pattern('@Transactional')
        self.ppr.set_input("//comment\n@Transactional\nlong funcname() { }\n")
        eq_("@Transactional\n", self.ppr.get_output())

    def test_simple_match_in_middle_of_line(self):
        self.ppr.set_pattern('Propagation.REQUIRES_NEW')
        self.ppr.set_input("//comment\n@Transactional(blah=Propagation.REQUIRES_NEW)\nlong funcname() { }\n")
        eq_("@Transactional(blah=Propagation.REQUIRES_NEW)\n", self.ppr.get_output())

    def test_set_config(self):
        conf = {}
        conf['regex_pattern'] = 'abc'
        self.ppr.set_config(conf)
        eq_(re.compile('abc'), self.ppr.pattern)

