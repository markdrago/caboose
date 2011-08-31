from nose.tools import *
from unittest import TestCase

from files.file_preprocess_js_subset import FilePreProcessJsSubset

class FilePreProcessJsSubsetTests(TestCase):
    def setUp(self):
        self.jspp = FilePreProcessJsSubset()

    def test_removes_all_lines_if_no_js_lines_found(self):
        self.jspp.set_input("<html>\n<head>\n</head>\n<body>\n</body>\n</html>\n")
        eq_("", self.jspp.get_output())

    def test_leaves_js_obvious(self):
        text = "<html>\n"
        text += "<head>\n"
        text += "<script>\n"
        text += "javascript here\n"
        text += "</script>\n"
        text += "</head>\n"
        text += "<body></body></html>\n"
        self.jspp.set_input(text)
        eq_("javascript here\n", self.jspp.get_output())

    def test_capitalized_tags(self):
        text = "before\n"
        text += "<SCRIPT>\n"
        text += "javascript here\n"
        text += "</SCRIPT>\n"
        text += "after\n"
        self.jspp.set_input(text)
        eq_("javascript here\n", self.jspp.get_output())

    def test_extra_attributes_in_script_tag(self):
        text = "before\n"
        text += "<script type=\"text/javascript\">\n"
        text += "javascript here\n"
        text += "</script>\n"
        text += "after\n"
        self.jspp.set_input(text)
        eq_("javascript here\n", self.jspp.get_output())

    def test_multiple_javascript_blocks(self):
        text = "before\n"
        text += "<script>\n"
        text += "javascript here\n"
        text += "</script>\n"
        text += "middle\n"
        text += "<script>\n"
        text += "more js here\n"
        text += "</script>\n"
        text += "after\n"
        self.jspp.set_input(text)
        eq_("javascript here\nmore js here\n", self.jspp.get_output())

