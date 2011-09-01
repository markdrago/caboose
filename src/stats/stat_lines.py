from statistic import Statistic
from files.file_preprocessor_factory import FilePreProcessorFactory

class StatLines(Statistic):
    def __init__(self):
        self.preprocessor_factory = FilePreProcessorFactory()

    def get_stat(self):
        preprocessor = self.preprocessor_factory.get_preprocessor('js_subset')
        return sum([self.get_single_file_stat(f, preprocessor) for f in self.files])

    @classmethod
    def get_name(clazz):
        return "lines"

    def get_single_file_stat(self, filename, preprocessor):
        f = open(filename, "r")
        contents = f.read()
        f.close()
        
        if preprocessor is not None:
            preprocessor.set_input(contents)
            contents = preprocessor.get_output()
        
        return len(contents.split("\n")) - 1

    def set_preprocessor_factory(self, factory):
        self.preprocessor_factory = factory

