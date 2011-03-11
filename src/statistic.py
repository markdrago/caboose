from subprocess import Popen, PIPE

class Statistic(object):
    def set_files(self, files):
        self.files = files

    def get_result_from_shell(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        p.wait()
        output = p.stdout.read()
        return output

