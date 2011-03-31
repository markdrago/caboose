from statistic import Statistic

class AbstractJavaCcnStat(Statistic):
    def get_ccn_list(self):
        filestr = ' '.join(self.files)
        cmd = "echo %s | xargs javancss -function | head -n -4 | tail -n +2 | awk '{print $3}'"
        cmd = cmd % (filestr,)
        output = self.get_result_from_shell(cmd)
        output = output.strip()
        if output == "":
            return []
        
        results = []
        for outline in output.split('\n'):
            outline = outline.strip()
            if outline.isdigit():
                results.append(int(outline))
        
        return results

