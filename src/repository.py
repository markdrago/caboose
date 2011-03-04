class Repository(object):
    def switch_to_before_date(self, date):
        raise Exception("switch_to_before_date() must be implemented by sublass")

    def get_date_of_earliest_commit(self):
        raise Exception("get_date_of_earliest_commit() must be implemented by subclass")

