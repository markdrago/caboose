from subprocess import Popen, PIPE

class StatLines(object):
    def set_directories(self, *dirs):
        self.dirs = dirs

    def get_stat(self):
        basecmd = "/usr/bin/find %s -type f -name '*.java' -print0 2> /dev/null | /usr/bin/wc -l --files0-from=- | /usr/bin/tail -n 1 | awk '{print $1}'"

        total = 0        
        for directory in self.dirs:
            p = Popen(basecmd % (directory,), shell=True, stdout=PIPE)
            p.wait()
            output = p.stdout.readline()
            output = output.strip()
            if output.isdigit():
                total += int(output)
        return total

