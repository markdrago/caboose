from nose.tools import *
from unittest import TestCase

from files.file_preprocess_regex import FilePreProcessRegex

class FilePreProcessRegexTests(TestCase):
    def setUp(self):
        self.ppr = FilePreProcessRegex()
    
    
