import os
from mercurial import hg, ui, commands, cmdutil
from datetime import datetime

from repository import Repository

dateformat = '%Y-%m-%d %H:%M:%S'

#A repository must implement the following functions:
#  get_date_of_earliest_commit(self):
#    returns a datetime object
#  get_revision_before_date(self, date)
#    date is a datetime object
#    returns an object that can be passed to switch_to_revision()
#  switch_to_revision(self, rev)
#    rev is an object that was returned from get_revision_before_date()
#  get_base_directory(self)
#    returns a string which is the full path to the repository base

class MercurialRepository(object):
    def __init__(self, directory='.', init=False):
        self.ui = ui.ui()
        self.ui.setconfig('ui', 'quiet', True)
        if init and not os.path.isdir(os.path.join(directory, '.hg')):
            commands.init(self.ui, directory)
        self.repo = hg.repository(self.ui, directory)

    def switch_to_revision(self, rev):
        commands.update(self.ui, self.repo, rev=rev)

    def switch_to_date(self, date):
        datestr = self.date_as_string(date)
        commands.update(self.ui, self.repo, date=datestr)
    
    def get_revision_before_date(self, date):
        datestr = self.date_as_string(date)
        rev = int(cmdutil.finddate(self.ui, self.repo, "<%s" % datestr))
        return self.repo[rev].hex()
    
    def switch_to_before_date(self, date):
        datestr = self.date_as_string(date)
        commands.update(self.ui, self.repo, date="<%s" % datestr)

    def get_date_of_earliest_commit(self):
        chgset = self.repo[0]
        return datetime.fromtimestamp(chgset.date()[0])

    def get_base_directory(self):
        return self.repo.root

    def get_working_directory_parent_revision(self):
        working_directory = self.repo[None]
        chgset = working_directory.p1()
        return chgset.hex()

    def get_ui(self):
        return self.ui
        
    def get_repo(self):
        return self.repo

    def date_as_string(self, date):
        return date.strftime(dateformat)
