from stat_java_ncss import StatJavaNcss
from stat_lines import StatLines
from stat_java_mean_ccn import StatJavaMeanCcn
from stat_java_ccn_func_count import StatJavaCcnFuncCount
from stat_percentage import StatPercentage

class StatFactory(object):
    def __init__(self):
        self.stat_classes = (StatLines, StatJavaNcss, StatJavaMeanCcn, StatJavaCcnFuncCount, StatPercentage)

    def get_stat(self, statname, conf={}):
        stat = None
        for statclass in self.stat_classes:
            if statname == statclass.get_name():
                stat = statclass()
                break

        if stat is None:
            raise StatDoesNotExistException()
        
        stat.set_config(conf)
        return stat

class StatDoesNotExistException(Exception):
    pass

