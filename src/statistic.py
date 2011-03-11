from subprocess import Popen, PIPE

class Statistic(object):
    def set_files(self, files):
        self.files = files

    def get_stat(self):
        return self.get_multiple_file_stat()

    def get_single_file_stat_from_shell(self, cmd, filename):
        output = self.get_result_from_shell(cmd % (filename,))
        output = output.split('\n')[0]
        output = output.strip()
        if output.isdigit():
            return int(output)
        return 0

    def get_result_from_shell(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        p.wait()
        output = p.stdout.read()
        return output

