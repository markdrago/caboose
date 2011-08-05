import json
from datetime import datetime

class ResultsPackage(object):
    def __init__(self):
        self.results = {}
        self.description = None
        self.datatype = None
    
    def add_result(self, date, result):
        if date not in self.results:
            self.results[date] = {}

        self.results[date] = result
    
    def add_results_from_json(self, jsontxt):
        jsondata = json.loads(jsontxt)
        if 'stats' not in jsondata:
            return
        for (date, value) in jsondata['stats'].items():
            dt = self._get_datetime_from_javascript_date(date)
            self.add_result(dt, value)

    def get_result(self, date):
        return self.results[date]

    def get_date_count(self):
        return len(self.results.keys())

    def get_json(self):
        json_results = self._get_results_with_javascript_dates()
        complete = { "stats" : json_results }
        if self.description is not None:
            complete['description'] = self.description
        if self.datatype is not None:
            complete['datatype'] = self.datatype
        return json.dumps(complete, indent=2)

    def write_json_results(self, outfile):
        res = self.get_json()
        with file(outfile, "w") as f:
            f.write(res)

    def get_dates(self):
        return self.results.keys()

    def set_description(self, description):
        self.description = description

    def set_datatype(self, datatype):
        self.datatype = datatype

    def _get_results_with_javascript_dates(self):
        #convert datetime keys in to javascript time (ms since epoch)
        js_results = {}
        for date in self.results.keys():
            unixtime = date.strftime("%s")
            js_time = int(unixtime) * 1000
            js_results[js_time] = self.results[date]
        return js_results

    def _get_datetime_from_javascript_date(self, js_time):
        epoch = float(js_time) / 1000
        return datetime.fromtimestamp(epoch)

