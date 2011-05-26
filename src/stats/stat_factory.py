from stat_java_ncss import StatJavaNcss
from stat_lines import StatLines
from stat_java_mean_ccn import StatJavaMeanCcn
from stat_java_ccn_func_count import StatJavaCcnFuncCount

class StatFactory(object):
    def get_stat(self, statname):
        if statname == 'java_ncss':
            return StatJavaNcss()
        elif statname == 'lines':
            return StatLines()
        elif statname == 'java_mean_ccn':
            return StatJavaMeanCcn()
        elif statname == 'java_ccn_func_count':
            return StatJavaCcnFuncCount()

        raise StatDoesNotExistException()

class StatDoesNotExistException(Exception):
    pass

