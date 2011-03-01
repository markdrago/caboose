from tempfile import mkdtemp
from uuid import uuid4
from os import path

from mercurial import hg, ui, commands

def create_repo(directory=None, hg_ui=None):
    '''create a mercurial repository in a temp directory'''
    if directory is None:
        directory = mkdtemp('-gbtests')
    if hg_ui is None:
        hg_ui = ui.ui()
    commands.init(hg_ui, directory)
    
    repo = hg.repository(hg_ui, directory)
    
    return (repo, directory, ui)

def create_changesets(repo, num=1, hg_ui=None, dates=[]):
    if hg_ui is None:
        hg_ui = ui.ui()

    for i in range(num):
        filename = _create_random_file(repo.root)
        commands.add(hg_ui, repo, filename)
        
        date=None
        if i < len(dates):
            date=dates[i]
        commands.commit(hg_ui, repo, date=date, message="creating %s" % (filename,))

def _create_random_file(directory):
    filename = path.join(directory, str(uuid4()))
    with open(filename, 'w') as f:
        f.write(filename)
        f.close()
    return filename

def get_working_directory_parent_revision(repo):
    working_directory = repo[None]
    chgset = working_directory.p1()
    return chgset.rev()

def get_repo_for_directory(directory):
    return hg.repository(ui.ui(), directory)

