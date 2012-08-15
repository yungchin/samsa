import mock
import unittest2

from samsa.batch import Batch
from samsa.cluster import Cluster


class BatchTestCase(unittest2.TestCase):
    def setUp(self):
        self.cluster = mock.Mock(spec=Cluster)

    def test_context_manager(self):
        batch = Batch(self.cluster)
        batch.flush = mock.Mock(side_effect=batch.flush)
        with batch:
            batch.publish('topic', ('hello', 'world'))
            self.assertEqual(len(batch.pending), 1)
        self.assertEqual(len(batch.pending), 0)
        self.assertEqual(batch.flush.call_count, 1)

    def test_context_manager_on_failure(self):
        batch = Batch(self.cluster)
        batch.flush = mock.Mock(side_effect=batch.flush)
        try:
            with batch:
                batch.publish('topic', ('hello', 'world'))
                self.assertEqual(len(batch.pending), 1)
                raise Exception
        except:
            pass
        self.assertEqual(len(batch.pending), 0)
        self.assertEqual(batch.flush.call_count, 1)
