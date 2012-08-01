from unittest import TestCase

from samsa import metrics


class TestMetrics(TestCase):

    def test_singleton(self):
        self.assertEquals(
            type(metrics.BaseMetricReporter.instance()),
            metrics.BaseMetricReporter
        )
        self.assertEquals(
            type(metrics.MemoryBackedReporter.instance()),
            metrics.MemoryBackedReporter
        )
