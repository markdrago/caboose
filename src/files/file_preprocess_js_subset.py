class FilePreProcessJsSubset(object):
    def __init__(self):
        self.full_file_contents = ""

    def set_input(self, contents):
        self.full_file_contents = contents
    
    def get_output(self):
        result = ""
        in_tags = False
        for line in self.full_file_contents.split("\n"):
            if "<script" in line.lower():
                in_tags = True
                continue
            if "</script" in line.lower():
                in_tags = False
                continue
            if in_tags:
                result += line + "\n"
        return result

