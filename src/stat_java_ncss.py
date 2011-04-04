from statistic import Statistic
import os

class StatJavaNcss(Statistic):
    def __init__(self):
        Statistic.__init__(self)
        self._set_ncss_command("javancss -ncss | sed -e 's/Java NCSS: //'")

    def get_name(self):
        return "ncss"

    def get_stat(self):
        filename = self.write_filenames_to_temp_file()
        
        cmd = "xargs -r -a %s %s"
        cmd = cmd % (filename, self.ncss_command)

        output = self.get_result_from_shell(cmd)

        os.remove(filename)

        #xargs could run javancss more than once so we need to
        #handle more than one line of output
        total = 0
        for outline in output.split('\n'):
            outline = outline.strip()
            if outline.isdigit():
                total += int(outline)
        return total

    def _set_ncss_command(self, cmd):
        self.ncss_command = cmd

