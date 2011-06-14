from stat_java_ncss import StatJavaNcss
from stat_lines import StatLines
from stat_java_mean_ccn import StatJavaMeanCcn
from stat_java_ccn_func_count import StatJavaCcnFuncCount

class StatFactory(object):
    def __init__(self):
        self.stat_classes = (StatLines, StatJavaNcss, StatJavaMeanCcn, StatJavaCcnFuncCount)

    def get_stat(self, statname):
        for statclass in self.stat_classes:
            if statname == statclass.get_name():
                return statclass()

        raise StatDoesNotExistException()

class StatDoesNotExistException(Exception):
    pass

