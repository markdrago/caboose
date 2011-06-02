from nose.tools import *
from unittest import TestCase

import json

from results.results_index import ResultsIndex

class ResultsIndexTests(TestCase):
    def setUp(self):
        self.ri = ResultsIndex()

    def test_results_index_creates_json_for_one_result(self):
        statdesc = "statdesc"
        outfile = "outfile"
        self.ri.add_result(statdesc, outfile)

        actual = json.loads(self.ri.get_index())

        ok_('stats' in actual)
        eq_(1, len(actual['stats']))
        eq_(statdesc, actual['stats'][0]['description'])
        eq_(outfile, actual['stats'][0]['filename'])

