import json

class ConfigParser(object):
    def parse_text(self, text):
        return json.loads(text)

    def parse_file(self, filename):
        with open(filename, "r") as f:
            return self.parse_text(f.read())

