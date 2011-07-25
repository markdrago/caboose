import json

distributable = (
    'repodir',
    'dirs',
    'glob',
    'start_time_delta',
    'datapoint_time_delta'
)

class ConfigParser(object):
    def parse_file(self, filename):
        with open(filename, "r") as f:
            return self.parse_text(f.read())

    def parse_text(self, text):
        conf = json.loads(text)
        self.distribute_global_options_to_stats(conf)
        return conf

    def distribute_global_options_to_stats(self, conf):
        for dist in distributable:
            if dist not in conf:
                continue
            for i in range(len(conf['stats'])):
                if dist in conf['stats'][i]:
                    continue
                conf['stats'][i][dist] = conf[dist]

