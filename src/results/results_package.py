import json

class ResultsPackage(object):
    def __init__(self):
        self.results = {}
    
    def add_result(self, date, result):
        if date not in self.results:
            self.results[date] = {}

        self.results[date] = result
    
    def get_result(self, date):
        return self.results[date]

    def get_date_count(self):
        return len(self.results.keys())

    def get_json(self):
        json_results = self._get_results_with_javascript_dates()
        complete = { "stats" : json_results }
        return json.dumps(complete, indent=2)

    def write_json_results(self, outfile):
        res = self.get_json()
        with file(outfile, "w") as f:
            f.write(res)

    def get_dates(self):
        return self.results.keys()

    def _get_results_with_javascript_dates(self):
        #convert datetime keys in to javascript time (ms since epoch)
        js_results = {}
        for date in self.results.keys():
            unixtime = date.strftime("%s")
            js_time = int(unixtime) * 1000
            js_results[js_time] = self.results[date]
        return js_results

