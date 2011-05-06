from abstract_java_ccn_stat import AbstractJavaCcnStat

class StatJavaCcnFuncCount(AbstractJavaCcnStat):
    def set_ccn_limit(self, ccn_limit):
        self.ccn_limit = ccn_limit

    def get_name(self):
        return "ccnfunctioncount"
        
    def get_stat(self):
        ccns = self.get_ccn_list()
        return len([ccn for ccn in ccns if ccn >= self.ccn_limit])

