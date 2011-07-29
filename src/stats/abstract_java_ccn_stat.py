from statistic import Statistic
import os

class AbstractJavaCcnStat(Statistic):
    def get_ccn_list(self):
        filename = self.write_filenames_to_temp_file()
        
        cmd = "javancss -function @%s | egrep '^[[:space:]]*[[:digit:]]+' | awk '{print $3}'"
        cmd = cmd % (filename,)

        output = self.get_result_from_shell(cmd)
        
        os.remove(filename)
        
        output = output.strip()
        if output == "":
            return []
        
        results = []
        for outline in output.split('\n'):
            outline = outline.strip()
            if outline.isdigit():
                results.append(int(outline))
        
        return results

