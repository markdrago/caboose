from subprocess import Popen, PIPE

class StatLines(object):
    def __init__(self, dirs):
        self.dirs = dirs

    def get_stat(self):
        basecmd = "/usr/bin/find %s -type f -name '*.java' -print0 | /usr/bin/wc -l --files0-from=- | /usr/bin/tail -n 1 | awk '{print $1}'"

        total = 0        
        for directory in self.dirs:
            p = Popen(basecmd % (directory,), shell=True, stdout=PIPE)
            p.wait()
            output = p.stdout.readline()
            total += int(output)
        return total

