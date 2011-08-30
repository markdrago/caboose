from nose.tools import *
from unittest import TestCase

from files.file_preprocess_js_subset import FilePreProcessJsSubset

class FilePreProcessJsSubsetTests(TestCase):
    def setUp(self):
        self.jspp = FilePreProcessJsSubset()

    def test_removes_all_lines_if_no_js_lines_found(self):
        self.jspp.set_full_file_contents("<html>\n<head>\n</head>\n<body>\n</body>\n</html>\n")
        eq_("", self.jspp.get_js_subset())

    def test_leaves_js_obvious(self):
        text = "<html>\n"
        text += "<head>\n"
        text += "<script>\n"
        text += "javascript here\n"
        text += "</script>\n"
        text += "</head>\n"
        text += "<body></body></html>\n"
        self.jspp.set_full_file_contents(text)
        eq_("javascript here\n", self.jspp.get_js_subset())

