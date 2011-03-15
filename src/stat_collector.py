from os import path
from datetime import datetime

from date_iterator import DateIterator
from repository_iterator import RepositoryIterator

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
        
        results = {}
        for date in ri:

            stat_results = {}
            for stat in self.stats:
                stat.set_files(self.files)
                stat_results[stat.get_name()] = stat.get_stat()

            self.print_one_day_results(date, stat_results)
            results[date] = stat_results

        return results

    def print_one_day_results(self, date, results):
        result_string = ""
        sep = ""
        for result in results.values():
            result_string += sep + "%.2f" % result
            sep = ","

        print "%s,%s" % (datetime.strftime(date, '%Y-%m-%d'), result_string)

