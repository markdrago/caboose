from os import path
from datetime import datetime

from date_iterator import DateIterator
from repository_iterator import RepositoryIterator
from results_package import ResultsPackage

class StatCollector(object):
    def __init__(self, repo, delta, files, stats, start=None,
                 end=datetime.now()):
        self.repo = repo
        self.timedelta = delta
        self.files = files
        self.stats = stats
        
        self.end = end
        self.start = start
        if self.start is None:
            self.start = self.repo.get_date_of_earliest_commit()

    def get_stats(self):
        di = DateIterator(self.start, self.end, self.timedelta)
        ri = RepositoryIterator(self.repo, di)
        
        results = ResultsPackage()
        for date in ri:

            for stat in self.stats:
                stat.set_files(self.files)
                stat_result = stat.get_stat()
                results.add_result(date, stat.get_name(), stat_result)

#            self.print_one_day_results(date, stat_results)

        return results

    def print_one_day_results(self, date, results):
        result_string = ""
        sep = ""
        for name, result in results.items():
            result_string += sep + "%s->%.2f" % (name, result)
            sep = ","

        print "%s,%s" % (datetime.strftime(date, '%Y-%m-%d'), result_string)

