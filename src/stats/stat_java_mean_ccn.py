from abstract_java_ccn_stat import AbstractJavaCcnStat

class StatJavaMeanCcn(AbstractJavaCcnStat):
    @classmethod
    def get_name(clazz):
        return "java_mean_ccn"
        
    def get_stat(self):
        ccns = self.get_ccn_list()
        if len(ccns) == 0:
            return 0

        return float(sum(ccns)) / len(ccns)

