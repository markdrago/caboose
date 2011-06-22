from abstract_java_ccn_stat import AbstractJavaCcnStat

class StatJavaCcnFuncCount(AbstractJavaCcnStat):
    @classmethod
    def get_name(clazz):
        return "java_ccn_func_count"

    def set_config(self, conf):
        if 'ccn_limit' in conf:
            self.set_ccn_limit(conf['ccn_limit'])

    def set_ccn_limit(self, ccn_limit):
        self.ccn_limit = ccn_limit

    def get_stat(self):
        ccns = self.get_ccn_list()
        return len([ccn for ccn in ccns if ccn >= self.ccn_limit])

