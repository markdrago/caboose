from statistic import Statistic

class StatPercentage(Statistic):
    @classmethod
    def get_name(clazz):
        return "percentage"

    def get_stat(self, values):
        #not sure that there is anything smarter to do here for div/0
        if values[1] == 0:
            return 0
        return (float(values[0]) / float(values[1]) * 100)

