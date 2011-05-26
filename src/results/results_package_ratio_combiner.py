from results_package import ResultsPackage

class ResultsPackageRatioCombiner(object):
    def combine(self, rp1, rp2, orig_stat_name, combo_stat_name):
        result = ResultsPackage()
        
        for date in rp1.get_dates():
            val1 = rp1.get_result(date, orig_stat_name)
            val2 = rp2.get_result(date, orig_stat_name)
            result.add_result(date, combo_stat_name, float(val1) / val2)
        
        return result

