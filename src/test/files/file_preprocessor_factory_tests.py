from nose.tools import *
from unittest import TestCase

from files.file_preprocessor_factory import FilePreProcessorFactory
from files.file_preprocessor_factory import FilePreProcessorDoesNotExistException
from files.file_preprocess_js_subset import FilePreProcessJsSubset

class FilePreProcessorFactoryTests(TestCase):
    def setUp(self):
        self.fppf = FilePreProcessorFactory()

    def test_get_js_subset_preprocessor(self):
        pp = self.fppf.get_preprocessor(FilePreProcessJsSubset.get_name())
        eq_(type(pp), FilePreProcessJsSubset)

    @raises(FilePreProcessorDoesNotExistException)
    def test_throws_exception_for_nonsense_preprocessor_name(self):
        pp = self.fppf.get_preprocessor('non-existant preprocessor')

