from summed_stat import SummedStat

class StatJavaNcss(SummedStat):
    def get_single_file_stat(self, filename):
        cmd = "javancss -ncss %s | sed -e 's/Java NCSS: //'"
        return self.get_single_file_stat_from_shell(cmd, filename)

