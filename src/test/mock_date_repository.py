class MockDateRepository(object):
    def __init__(self, date_revs, directory='.'):
        self.latest_rev_requested = None
        self.directory = directory
        self.date_revs = date_revs
        self.dates = self.date_revs.keys()
        self.dates.sort()
    
    def get_base_directory(self):
        return self.directory

    def get_revision_before_date(self, needle):
        if needle < self.dates[0]:
            raise Exception

        for date in self.dates:
            if needle == date:
                return self.date_revs[date]
            if needle < date:
                return self.date_revs[prev]
            prev = date

        raise Exception

    def switch_to_revision(self, rev):
        self.latest_rev_requested = rev

    def get_date_of_earliest_commit(self):
        return self.dates[0]

