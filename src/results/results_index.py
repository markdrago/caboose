import json
from os import path

class ResultsIndex(object):
    def __init__(self):
        self.stats = []

    def add_result(self, description, filename):
        self.stats.append(self.create_result(description, filename))
    
    def create_result(self, description, filename):
        return { 'description': description, 'filename': filename }

    def get_index(self):
        output = { 'stats' : self.stats }
        return json.dumps(output, indent = 2)

    def write_index(self, directory):
        res = self.get_index()

        outfile = path.join(directory, "index.json")
        with file(outfile, "w") as f:
            f.write(res)

