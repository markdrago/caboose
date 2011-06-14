from results_package import ResultsPackage

class ResultsPackageRatioCombiner(object):
    def combine(self, rp1, rp2):
        result = ResultsPackage()
        
        for date in rp1.get_dates():
            val1 = rp1.get_result(date)
            val2 = rp2.get_result(date)
            result.add_result(date, float(val1) / val2)
        
        return result

