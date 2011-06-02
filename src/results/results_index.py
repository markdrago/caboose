import json

class ResultsIndex(object):
    def __init__(self):
        self.stats = []

    def add_result(self, description, filename):
        self.stats.append(self.create_result(description, filename))
    
    def create_result(self, description, filename):
        return { 'description': description, 'filename': filename }

    def get_index(self):
        output = { 'stats' : self.stats }
        return json.dumps(output)

