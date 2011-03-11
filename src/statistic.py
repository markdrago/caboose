from subprocess import Popen, PIPE

class Statistic(object):
    def set_files(self, files):
        self.files = files
    
    def get_single_file_stat_from_shell(self, cmd, filename):
        p = Popen(cmd % (filename,), shell=True, stdout=PIPE)
        p.wait()
        output = p.stdout.readline()
        output = output.strip()
        if output.isdigit():
            return int(output)
        return 0

