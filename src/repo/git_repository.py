import os
import datetime
from subprocess import Popen, PIPE

class GitRepository:
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
        #TODO: get date by doing something like this:
        #git --git-dir ~/Code/core-git/.git log -1
        #git log --date-order --reverse -1 --format=%cd --date=iso
        #parse date to a datetime object
        dateformat = '%Y-%m-%d %H:%M:%S'
        return datetime()
    
    def add(self, filename):
        self.run_git("add %s" % (filename,))
    
    def run_git(self, cmd):
        cmd = "git --git-dir %s/.git --work-tree %s %s" % (self.directory, self.directory, cmd)
        return self.get_cmd_output(cmd)

    def get_cmd_output(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        (stdout_data, stderr_data) = p.communicate()
        return stdout_data

class GitRepositoryException(Exception):
    pass

