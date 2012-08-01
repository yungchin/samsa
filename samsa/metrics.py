import time

from collections import defaultdict
from contextlib import contextmanager

PRECISION = {
    'second': "%.0f",
    'millisecond': "%.3f",
    'microsecond': "%.6f",
}


class MetricsInterface(object):

    @contextmanager
    def timer(self, name, precision='microsecond'):
        """A context manager which will report the time of `name`.
        """
        start = time.time()
        yield
        self.histogram(
            'timer.' + name,
            PRECISION[precision] % (time.time() - start)
        )

    def timer_iter(self, iterable, name):
        """Time each call to next().
        """

        while True:
            try:
                with self.timer(name):
                    val = iterable.next()
            except StopIteration:
                return
            yield val


    def gauge(self, name, val):
        """Record `value` along with `name`.
        """
        raise NotImplementedError

    def count(self, name, val):
        """Add `val` to `name`.
        """
        raise NotImplementedError

    def histogram(self, name, val):
        """Use resevoir sampling to construct a histogram of values.
        """
        raise NotImplementedError
    
    def export_histogram(self):
        raise NotImplementedError


class MemoryBackedMetrics(MetricsInterface):

    def __init__(self):
        self.gauges = defaultdict(list)
        self.count = defaultdict(int)

    def gauge(self, name, val):
        self.gauges[name].append(val)

    def count(self, name, val):
        self.count[name] += val

    def histogram(self, name, val):
        """histogram == gauge in In-memort impl.
        """
        self.gauge(name, val)

    def export_histogram(self):
        total = {}
        for key in self.gauges:
            hist = defaultdict(int)
            for i in self.gauges[key]:
                hist[i] += 1
            total[key] = hist

        return total
