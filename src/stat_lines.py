from summed_stat import SummedStat

class StatLines(SummedStat):
    def get_single_file_stat(self, filename):
        cmd = "/usr/bin/wc -l %s | /usr/bin/tail -n 1 | awk '{print $1}'"
        return self.get_single_file_stat_from_shell(cmd, filename)

