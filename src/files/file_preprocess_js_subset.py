class FilePreProcessJsSubset(object):
    def __init__(self):
        self.full_file_contents = ""

    @classmethod
    def get_name(clazz):
        return 'js_subset'

    def set_input(self, contents):
        self.full_file_contents = contents
    
    def set_config(self, conf):
        pass
    
    def get_output(self):
        result = ""
        in_tags = False
        for line in self.full_file_contents.split("\n"):
            line = line.lower()
            if "<script" in line and "</script" not in line:
                in_tags = True
                continue
            if "</script" in line:
                in_tags = False
                continue
            if in_tags:
                result += line + "\n"
        return result

