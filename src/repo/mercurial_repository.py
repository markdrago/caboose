import os
from mercurial import hg, ui, commands, cmdutil
from datetime import datetime, timedelta

dateformat = '%Y-%m-%d %H:%M:%S'

#A repository must implement the following functions:
#  get_date_of_earliest_commit(self):
#    returns a datetime object
#  get_revision_before_date(self, date)
#    date is a datetime object
#    returns an object that can be passed to switch_to_revision()
#    should only match commits on the current branch (never switch branches)
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
        datestr = "<%s" % self.date_as_string(date)
        branch = self.repo[None].branch()
        self.ui.pushbuffer()
        commands.log(self.ui, self.repo, branch=[branch], template="{node}\n", date=datestr, rev='', user='', limit=10)
        hexids = self.ui.popbuffer()

        #loop over up to 10 changesets to find first non-bogus one
        for hexid in hexids.split():
            if not self.changeset_is_bogus(self.repo[hexid]):
                return hexid.strip()
        return None

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

    def create_and_switch_to_branch(self, branchname):
        commands.branch(self.ui, self.repo, label=branchname)

    def changeset_is_bogus(self, chgset):
        return self.changeset_is_bogus_due_to_commit_date_history(chgset)

    def changeset_is_bogus_due_to_commit_date_history(self, chgset, depth=10):
        if depth == 0:
            return False
        parent = self.get_parent_chgset_on_same_branch(chgset)
        if self.parent_and_child_dates_are_too_far_in_wrong_direction(parent, chgset):
            return True
        else:
            return self.changeset_is_bogus_due_to_commit_date_history(parent, depth-1)

    #this tries to stay on the same branch, but if there is a fast-forward
    #merge in the repo somewhere it will just return the single parent that
    #is on a different branch
    def get_parent_chgset_on_same_branch(self, chgset):
        branch = chgset.branch()
        parents = chgset.parents()
        if len(parents) == 0:
            return None
        if len(parents) > 1 and parents[1].branch() == branch:
            return parents[1]
        return parents[0]


    def parent_and_child_dates_are_too_far_in_wrong_direction(self, parent, child):
        pdate = self.datetime_from_hg_date(parent.date())
        cdate = self.datetime_from_hg_date(child.date())
        delta = cdate - pdate

        #how negative the difference can be before it is bogus
        limit = timedelta(seconds=-86400)   #one day

        #if the real delta is more negative than the limit
        if delta < limit:
            return True
        return False

    def get_ui(self):
        return self.ui
        
    def get_repo(self):
        return self.repo

    def date_as_string(self, date):
        return date.strftime(dateformat)

    def datetime_from_hg_date(self, date):
        return datetime.fromtimestamp(int(date[0]))

