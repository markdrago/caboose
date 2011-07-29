from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

class Statistic(object):
	#TODO: move to a FileStatistic or something like that b/c
	# it only deals with files and there are other stats which don't
    def set_files(self, files):
        self.files = files

    #can be overriden by individual stats
    def set_config(self, conf):
        pass

    #TODO: move to some utils class
    def get_result_from_shell(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        (stdout_data, stderr_data) = p.communicate()
        return stdout_data

    #TODO: move to some utils class
    def write_filenames_to_temp_file(self):
        filestr = "\n".join(self.files)

        f = NamedTemporaryFile(mode='w', delete=False)
        f.write(filestr)
        f.close()
        
        return f.name

