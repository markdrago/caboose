from statistic import Statistic
from files.file_preprocessor_factory import FilePreProcessorFactory

class StatLines(Statistic):
    def __init__(self):
        self.preprocessor_factory = FilePreProcessorFactory()
        self.preprocessor = None

    def get_stat(self):
        return sum([self.get_single_file_stat(f) for f in self.files])

    @classmethod
    def get_name(clazz):
        return "lines"

    def set_config(self, conf):
        if 'preprocessor' in conf:
            self.preprocessor = self.get_preprocessor(conf['preprocessor'])
            self.preprocessor.set_config(conf)

    def get_single_file_stat(self, filename):
        f = open(filename, "r")
        contents = f.read()
        f.close()
        
        if self.preprocessor is not None:
            self.preprocessor.set_input(contents)
            contents = self.preprocessor.get_output()
        
        return len(contents.split("\n")) - 1

    def get_preprocessor(self, name):
        if name is None:
            return None
        return self.preprocessor_factory.get_preprocessor(name)

    def set_preprocessor_factory(self, factory):
        self.preprocessor_factory = factory

    def set_preprocessor_name(self, name):
        self.preprocessor_name = name

