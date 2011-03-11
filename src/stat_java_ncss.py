from statistic import Statistic
from shell_stat import ShellStat
from summed_stat import SummedStat

class StatJavaNcss(Statistic, ShellStat, SummedStat):
    def get_single_file_cmd(self):
        return "javancss -ncss %s | sed -e 's/Java NCSS: //'"

