class Repository(object):
    def get_date_of_earliest_commit(self):
        raise Exception("get_date_of_earliest_commit() must be implemented by subclass")

    def get_revision_before_date(self, date):
        raise Exception("get_revision_before_date() must be implemented by subclass")

    def switch_to_revision(self, rev):
        raise Exception("switch_to_revision() must be implemented by subclass")

    def get_base_directory(self):
        raise Exception("get_base_revision() must be implemented by subclass")
