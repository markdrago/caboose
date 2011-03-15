from statistic import Statistic

class StatJavaNcss(Statistic):
    def get_stat(self):
        filestr = ' '.join(self.files)
        cmd = "echo %s | xargs javancss -ncss | sed -e 's/Java NCSS: //'"
        cmd = cmd % (filestr,)
        output = self.get_result_from_shell(cmd)

        #xargs could run javancss more than once so we need to
        #handle more than one line of output
        total = 0
        for outline in output.split('\n'):
            outline = outline.strip()
            if outline.isdigit():
                total += int(outline)
        return total

