from subprocess import Popen, PIPE

class StatLines(object):
    def __init__(self, directory):
        self.directory = directory

    def get_stat(self):
        cmd = "/usr/bin/find %s -type f -name '*.java' -print0 | /usr/bin/wc -l --files0-from=- | /usr/bin/tail -n 1 | awk '{print $1}'" % (self.directory,)
        p = Popen(cmd, shell=True, stdout=PIPE)
        p.wait()
        output = p.stdout.readline()
        return int(output)

