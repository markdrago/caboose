from statistic import Statistic

class StatJavaMeanCcn(Statistic):
    def get_name(self):
        return "meanccn"
        
    def get_stat(self):
        filestr = ' '.join(self.files)
        cmd = "echo %s | xargs javancss -function | head -n -4 | tail -n +2 | awk '{print $3}'"
        cmd = cmd % (filestr,)
        output = self.get_result_from_shell(cmd)
        output = output.strip()
        if (output == ""):
            return 0

        total = 0
        file_count = 0
        for outline in output.split('\n'):
            outline = outline.strip()
            if outline.isdigit():
                file_count += 1
                total += int(outline)

        if file_count == 0:
            return 0

        return float(total) / file_count

