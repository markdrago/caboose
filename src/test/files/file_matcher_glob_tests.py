from nose.tools import *
from unittest import TestCase

import os
from shutil import rmtree
from tempfile import mkdtemp

from files.file_matcher_glob import FileMatcherGlob

class FileMatcherGlobTests(TestCase):
    def setUp(self):
        self.directory = mkdtemp('-caboose-file-matcher-glob-tests')

    def tearDown(self):
        rmtree(self.directory)

    def test_file_matcher_matches_against_glob(self):
        self.file_matcher = FileMatcherGlob("*.java")
        eq_(True, self.file_matcher.match("hello.java"))
        eq_(False, self.file_matcher.match("hello.java2"))

