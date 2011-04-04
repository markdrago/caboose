from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

class Statistic(object):
    def set_files(self, files):
        self.files = files

    def get_result_from_shell(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        p.wait()
        output = p.stdout.read()
        return output

    def write_filenames_to_temp_file(self):
        filestr = "\n".join(self.files)

        f = NamedTemporaryFile(mode='w', delete=False)
        f.write(filestr)
        f.close()
        
        return f.name

