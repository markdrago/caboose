class RepositoryIterator(object):
    def __init__(self, repo, date_iterator):
        self.repo = repo
        self.date_iterator = date_iterator.__iter__()
    
    def __iter__(self):
        return self
    
    def next(self):
        nextdate = self.date_iterator.next()
        rev = self.repo.get_revision_before_date(nextdate)
        self.repo.switch_to_revision(rev)

