from statistic import Statistic
from files.file_preprocessor_factory import FilePreProcessorFactory

class StatLines(Statistic):
    def __init__(self):
        self.preprocessor_factory = FilePreProcessorFactory()
        self.preprocessor_name = None

    def get_stat(self):
        preprocessor = self.get_preprocessor()
        return sum([self.get_single_file_stat(f, preprocessor) for f in self.files])

    @classmethod
    def get_name(clazz):
        return "lines"

    def set_config(self, conf):
        if 'preprocessor' in conf:
            self.set_preprocessor_name(conf['preprocessor'])

    def get_single_file_stat(self, filename, preprocessor):
        f = open(filename, "r")
        contents = f.read()
        f.close()
        
        if preprocessor is not None:
            print filename
            preprocessor.set_input(contents)
            contents = preprocessor.get_output()
        
        return len(contents.split("\n")) - 1

    def get_preprocessor(self):
        if self.preprocessor_name is None:
            return None
        return self.preprocessor_factory.get_preprocessor(self.preprocessor_name)

    def set_preprocessor_factory(self, factory):
        self.preprocessor_factory = factory

    def set_preprocessor_name(self, name):
        self.preprocessor_name = name

