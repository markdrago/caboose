from statistic import Statistic
from shell_stat import ShellStat
from summed_stat import SummedStat

class StatLines(Statistic, ShellStat, SummedStat):
    def get_single_file_cmd(self):
        return "/usr/bin/wc -l %s | /usr/bin/tail -n 1 | awk '{print $1}'"

