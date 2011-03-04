import os
from mercurial import hg, ui, commands, cmdutil
from datetime import datetime

from repository import Repository

class MercurialRepository(Repository):
    def __init__(self, directory='.', init=False):
        self.ui = ui.ui()
        if init and not os.path.isdir(os.path.join(directory, '.hg')):
            commands.init(self.ui, directory)
        self.repo = hg.repository(self.ui, directory)

    def switch_to_revision(self, rev):
        commands.update(self.ui, self.repo, rev=rev)

    def switch_to_date(self, date):
        commands.update(self.ui, self.repo, date=date)
    
    def get_revision_before_date(self, date):
        return int(cmdutil.finddate(self.ui, self.repo, "<%s" % date))
    
    def switch_to_before_date(self, date):
        commands.update(self.ui, self.repo, date="<%s" % date)

    def get_date_of_earliest_commit(self):
        chgset = self.repo[0]
        d = datetime.fromtimestamp(chgset.date()[0])
        return d.strftime("%Y-%m-%d %H:%M:%S")

    def get_working_directory_parent_revision(self):
        working_directory = self.repo[None]
        chgset = working_directory.p1()
        return chgset.rev()

    def get_ui(self):
        return self.ui
        
    def get_repo(self):
        return self.repo
