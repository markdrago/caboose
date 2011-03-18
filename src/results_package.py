import json

class ResultsPackage(object):
    def __init__(self):
        self.results = {}
        self.statnames = []
    
    def add_result(self, date, name, result):
        if date not in self.results:
            self.results[date] = {}

        if name not in self.statnames:
            self.statnames.append(name)

        self.results[date][name] = result
    
    def get_result(self, date, name):
        return self.results[date][name]

    def get_results_for_date(self, date):
        return self.results[date]

    def get_date_count(self):
        return len(self.results.keys())

    def get_json(self):
        json_results = self._get_results_with_javascript_dates()
        return json.dumps(json_results)

    def _get_results_with_javascript_dates(self):
        #convert datetime keys in to javascript time (ms since epoch)
        json_results = {}
        for date in self.results.keys():
            unixtime = date.strftime("%s")
            jsontime = int(unixtime) * 1000
            json_results[jsontime] = self.results[date]
        return json_results

