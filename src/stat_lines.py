from statistic import Statistic

class StatLines(Statistic):
    def get_stat(self):
        return sum([self.get_single_file_stat(f) for f in self.files])

    def get_single_file_stat(self, filename):
        cmd = "/usr/bin/wc -l %s | /usr/bin/tail -n 1 | awk '{print $1}'"

        output = self.get_result_from_shell(cmd % (filename,))
        output = output.split('\n')[0]
        output = output.strip()
        if output.isdigit():
            return int(output)
        return 0

