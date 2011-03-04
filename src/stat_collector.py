from date_iterator import DateIterator

from datetime import datetime
from repository_iterator import RepositoryIterator

class StatCollector(object):
    def __init__(self, repo, delta, dirs, stat_classes, start=None,
                 end=datetime.now()):
        self.repo = repo
        self.timedelta = delta
        self.dirs = dirs
        self.stat_classes = stat_classes
        
        self.end = end
        self.start = start
        if self.start is None:
            self.start = self.repo.get_date_of_earliest_commit()

    def get_stats(self):
        di = DateIterator(self.start, self.end, self.timedelta)
        ri = RepositoryIterator(self.repo, di)
        
        stat = self.stat_classes[0](self.dirs)
        
        results = {}
        for date in ri:
            results[date] = stat.get_stat()

        return results

