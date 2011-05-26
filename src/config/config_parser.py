import json

class ConfigParser(object):
    def parse_text(self, text):
        return json.loads(text)

