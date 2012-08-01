__license__ = """
Copyright 2012 DISQUS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import time

from collections import defaultdict
from contextlib import contextmanager

PRECISION = {
    'second': "%.0f",
    'millisecond': "%.3f",
    'microsecond': "%.6f",
}

_INSTANCES = {}

class BaseMetricReporter(object):

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
        pass

    def count(self, name, val):
        """Add `val` to `name`.
        """
        pass

    def histogram(self, name, val):
        """Use resevoir sampling to construct a histogram of values.
        """
        pass

    def export_histogram(self):
        pass

    @classmethod
    def instance(cls):
        if cls.__name__ not in _INSTANCES:
            _INSTANCES[cls.__name__] = cls()
        return _INSTANCES[cls.__name__]


class MemoryBackedReporter(BaseMetricReporter):

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
