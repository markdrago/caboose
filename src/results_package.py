class ResultsPackage(object):
    def __init__(self):
        self.results = {}
    
    def add_result(self, date, name, result):
        if date not in self.results:
            self.results[date] = {}
        self.results[date][name] = result
    
    def get_result(self, date, name):
        return self.results[date][name]

    def get_results_for_date(self, date):
        return self.results[date]

    def get_date_count(self):
        return len(self.results.keys())

