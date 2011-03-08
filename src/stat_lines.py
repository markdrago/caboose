from subprocess import Popen, PIPE

class StatLines(object):
    def set_files(self, files):
        self.files = files

    def get_stat(self):
        basecmd = "/usr/bin/wc -l %s | /usr/bin/tail -n 1 | awk '{print $1}'"

        total = 0        
        for f in self.files:
            p = Popen(basecmd % (f,), shell=True, stdout=PIPE)
            p.wait()
            output = p.stdout.readline()
            output = output.strip()
            if output.isdigit():
                total += int(output)
        return total

