from statistic import Statistic

class SummedStat(Statistic):
    def get_multiple_file_stat(self):
        total = 0
        for f in self.files:
            total += self.get_single_file_stat(f)
        return total

