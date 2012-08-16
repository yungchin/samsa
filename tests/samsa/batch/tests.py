import itertools
import mock
import unittest2

from samsa.batch import Batch
from samsa.test.integration import KafkaIntegrationTestCase


class BatchTestCase(KafkaIntegrationTestCase):
    def test_context_manager(self):
        batch = Batch(self.kafka_cluster)
        batch.flush = mock.Mock(side_effect=batch.flush)
        topic = self.kafka_cluster.topics['topic']
        messages = ('hello', 'world')
        with batch:
            batch.publish(topic, messages)
        messages = ('hello', 'world')
            self.assertEqual(len(batch.pending), 1)
        self.assertEqual(len(batch.pending), 0)
        self.assertEqual(batch.flush.call_count, 1)

        consumer_id_generator = ('consumer-%s' % i for i in itertools.count())
        def ensure_published():
            consumer = topic.subscribe(next(consumer_id_generator))
            self.assertEqual(list(itertools.islice(consumer, 2)), list(messages))

        self.assertPassesWithMultipleAttempts(ensure_published, 5)

    def test_context_manager_on_failure(self):
        batch = Batch(self.kafka_cluster)
        batch.flush = mock.Mock(side_effect=batch.flush)
        topic = self.kafka_cluster.topics['topic']
        try:
            with batch:
                batch.publish(topic, ('hello', 'world'))
                self.assertEqual(len(batch.pending), 1)
                raise Exception
        except:
            pass
        self.assertEqual(len(batch.pending), 0)
        self.assertEqual(batch.flush.call_count, 1)
