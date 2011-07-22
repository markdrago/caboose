#The purpose of this class is to look over the results files that have
#been created by other statistics and run stats on them.  This was originally
#created to gather stats on the # of lines of code in different projects
#and then go over those results and produce statistics on the % of code in a
#given project.

from results.results_package import ResultsPackage

class ResultsStatCollector(object):
    def __init__(self, stat):
        self.stat = stat

    def set_results_files(self, results_files):
        self.results_files = results_files
        self.create_all_results_packages()

    def create_all_results_packages(self):
        self.results = []
        for rf in self.results_files:
            self.results.append(self.get_results_package(rf))

    def get_results_package(self, results_file):
        rp = ResultsPackage()

        jsontext = ''
        with file(results_file, 'r') as f:
            jsontext = f.read()

        rp.add_results_from_json(jsontext)

        return rp

    def get_stats(self):
        rp = ResultsPackage()

        for dt in self.results[0].get_dates():
            values = [input_rp.get_result(dt) for input_rp in self.results]
            rp.add_result(dt, self.stat.get_stat(values))

        return rp

    def get_results(self):
        return self.results

    def set_results(self, results):
        self.results = results

