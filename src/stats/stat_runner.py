from os import path

from stats.stat_collector_factory import StatCollectorFactory

class StatRunner(object):
    def __init__(self):
        self.set_stat_collector_factory(StatCollectorFactory())
        self.conf = {}

    def run(self):
        stat_collector = self.create_stat_collector()
        outfile = self.get_outfile_location()

        results = stat_collector.get_stats()

        results.set_description(self.get_description())
        if self.conf_has_datatype():
            results.set_datatype(self.get_datatype())

        results.write_json_results(outfile)
        if self.include_in_results_index():
            self.results_index.add_result(self.get_description(), outfile)

    def set_conf(self, conf={}):
        self.conf = conf

    def set_output_directory(self, dirname):
        self.output_dir = dirname

    def set_stat_collector_factory(self, scf):
        self.stat_collector_factory = scf

    def create_stat_collector(self):
        return self.stat_collector_factory.get_stat_collector(self.conf)

    def get_outfile_location(self):
        return (path.join(self.output_dir, self.conf['outfile']))

    def get_description(self):
        return self.conf['description']

    def get_datatype(self):
        return self.conf['datatype']

    def conf_has_datatype(self):
        return 'datatype' in self.conf

    def set_results_index(self, results_index):
        self.results_index = results_index

    def include_in_results_index(self):
        key = 'include_in_results_index'
        if key in self.conf and self.conf[key] == False:
            return False
        return True

