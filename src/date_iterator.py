from datetime import timedelta

class DateIterator(object):
    def __init__(self, start, end, delta=timedelta(days=30)):
        self.start = start
        self.end = end
        self.delta = delta
        self.current = start

    def __iter__(self):
        return self

    def next(self):
        if self.current > self.end:
            raise StopIteration
        result = self.current
        self.current += self.delta
        return result

