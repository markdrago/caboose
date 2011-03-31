from statistic import Statistic

class StatJavaCcnFuncCount(Statistic):
    def __init__(self, ccn_limit):
        self.ccn_limit = ccn_limit

    def get_name(self):
        return "ccnfunctioncount"
        
    def get_stat(self):
        filestr = ' '.join(self.files)
        cmd = "echo %s | xargs javancss -function | head -n -4 | tail -n +2 | awk '{print $3}'"
        cmd = cmd % (filestr,)
        output = self.get_result_from_shell(cmd)
        output = output.strip()
        if (output == ""):
            return 0

        function_count = 0
        for outline in output.split('\n'):
            outline = outline.strip()
            if outline.isdigit():
                func_ccn = int(outline)
                if (func_ccn >= self.ccn_limit):
                    function_count += 1

        return function_count

