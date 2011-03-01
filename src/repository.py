from mercurial import hg, ui, commands

class HgSwitcher:
    def switch_to_revision(self, rev, directory='.'):
        hg_ui = ui.ui()
        repo = hg.repository(hg_ui, directory)
        commands.update(hg_ui, repo, rev=rev)

    def switch_to_date(self, date, directory='.'):
        hg_ui = ui.ui()
        repo = hg.repository(hg_ui, directory)
        commands.update(hg_ui, repo, date=date)
