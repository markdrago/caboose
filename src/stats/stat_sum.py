from statistic import Statistic

class StatSum(Statistic):
    @classmethod
    def get_name(clazz):
        return "sum"

    def get_stat(self, values):
        return sum(values)

