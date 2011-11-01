import os
from datetime import datetime
from subprocess import Popen, PIPE

class GitRepository(object):
    def __init__(self, directory, init=False):
        self.directory = directory
        if init:
            self.init_repository()
        if not os.path.isdir(os.path.join(self.directory, '.git')):
            raise GitRepositoryException("not a git directory")

    def init_repository(self):
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
        self.run_git("init")

    def get_date_of_earliest_commit(self):
        #TODO: this is kind of gross as it gets the dates of all commits and then 
        #just takes the first line of output.  "-1" in git does not do what we
        #want here, but there's probably still a better way
        output = self.run_git("log --date-order --reverse --format=%cd --date=iso")
        output = output.split("\n")
        datestr = output[0]
        return self.convert_git_date_to_datetime(datestr)
    
    def get_revision_before_date(self, date):
        datestr = date.isoformat()
        cmd = "log --before=%s -1 --format=%%H" % (datestr,)
        return self.run_git(cmd).strip()
    
    def switch_to_revision(self, rev):
        self.run_git("checkout -q %s" % (rev,))

    def get_base_directory(self):
        return self.run_git("rev-parse --show-toplevel").strip()
    
    def add(self, filename):
        self.run_git("add %s" % (filename,))
    
    def commit(self, message='default message', date=None):
        cmd = "commit -am '%s'" % (message,)

        if date is not None:
            datestr = date.isoformat()
            os.environ['GIT_COMMITTER_DATE'] = datestr

        self.run_git(cmd)

        if date is not None:
            del os.environ['GIT_COMMITTER_DATE']
    
    def run_git(self, cmd):
        cmd = "git --git-dir %s/.git --work-tree %s %s" % (self.directory, self.directory, cmd)
        return self.get_cmd_output(cmd)

    def get_cmd_output(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        (stdout_data, stderr_data) = p.communicate()
        return stdout_data

    def convert_git_date_to_datetime(self, gitdate):
        gitdate = gitdate.strip()
        
        #strip off timezone data, apparently python 2.x can not parse it with
        #things in the standard library, and a few hours in the grand scheme
        #of things does not matter that much
        if gitdate[-5] == '-' or gitdate[-5] == '+':
            gitdate = gitdate[:-6]
        
        return datetime.strptime(gitdate, '%Y-%m-%d %H:%M:%S')

class GitRepositoryException(Exception):
    pass

