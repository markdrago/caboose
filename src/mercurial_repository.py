from mercurial import hg, ui, commands

from repository import Repository

class MercurialRepository(Repository):

    def __init__(self, directory='.'):
        self.ui = ui.ui()
        self.repo = hg.repository(self.ui, directory)

    def switch_to_revision(self, rev):
        commands.update(self.ui, self.repo, rev=rev)

    def switch_to_date(self, date):
        commands.update(self.ui, self.repo, date=date)

