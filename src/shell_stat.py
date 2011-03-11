from subprocess import Popen, PIPE

class ShellStat(object):
    def get_single_file_stat(self, filename):
        cmd = self.get_single_file_cmd()
        p = Popen(cmd % (filename,), shell=True, stdout=PIPE)
        p.wait()
        output = p.stdout.readline()
        output = output.strip()
        if output.isdigit():
            return int(output)
        return 0

