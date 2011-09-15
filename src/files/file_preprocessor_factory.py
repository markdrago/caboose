from file_preprocess_js_subset import FilePreProcessJsSubset

class FilePreProcessorFactory(object):
    def get_preprocessor(self, name):
        classes = (FilePreProcessJsSubset,)

        for clazz in classes:
            if clazz.get_name() == name:
                return clazz()

        raise FilePreProcessorDoesNotExistException()

class FilePreProcessorDoesNotExistException(Exception):
    pass

