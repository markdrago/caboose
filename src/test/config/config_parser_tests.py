from nose.tools import *
from unittest import TestCase

from os import path
from shutil import rmtree
from tempfile import mkdtemp

from config.config_parser import ConfigParser

class ConfigParserTests(TestCase):
    def setUp(self):
        self.cp = ConfigParser()

    def test_parse_file(self):
        #create test config file
        directory = mkdtemp('-gb-config-parser-tests')
        filename = path.join(directory, "config")
        with open(filename, "w") as f:
            f.write("""{ "stats" : [ { "statname": "statnamehere" } ] }""")
        
        conf = self.cp.parse_file(filename)
        eq_('statnamehere', conf['stats'][0]['statname'])
        
        rmtree(directory)

    def test_parse_config_object(self):
        json = """{
            "stats": [
                {
                    "statname": "java_ncss",
                    "repodir": "/path/to/code/codedir",
                    "dirs": ["CodeDirectory"],
                    "glob": "*.java",
                    "start_time_delta": 2592000,
                    "datapoint_time_delta": 604800,
                    "outfile": "/path/to/outfile/shared_ncss.json"
                }
            ]
        }"""
        
        conf = self.cp.parse_text(json)
        
        eq_('java_ncss', conf['stats'][0]['statname'])
        eq_('/path/to/code/codedir', conf['stats'][0]['repodir'])
        eq_('CodeDirectory', conf['stats'][0]['dirs'][0])
        eq_('*.java', conf['stats'][0]['glob'])
        eq_(2592000, conf['stats'][0]['start_time_delta'])
        eq_(604800, conf['stats'][0]['datapoint_time_delta'])
        eq_('/path/to/outfile/shared_ncss.json', conf['stats'][0]['outfile'])

