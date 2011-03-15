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
        
        stat = self.stats[0]
        stat.set_files(self.files)
        
        results = {}
        for date in ri:
            results[date] = stat.get_stat()
            print "%s,%.2f" % (datetime.strftime(date, '%Y-%m-%d'), results[date])

        return results

