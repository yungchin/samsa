import itertools
from collections import defaultdict

from samsa.partitioners import random_partitioner


class Batch(object):
    def __init__(self, cluster, partitioner=random_partitioner):
        self.cluster = cluster
        self.pending = []
        self.partitioner = partitioner

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.flush()

    def publish(self, topic, data, key=None):
        """
        Queues a message (or messages) to be published upon flushing this batch.
        """
        # TODO: make sure that data is list/tuple on insert
        self.pending.append((topic, data, key))

    def flush(self):
        # Group the pending messages by topic/key.
        topics = defaultdict(lambda: defaultdict(list))
        for topic, data, key in self.pending:
            topics[topic][key].extend(data)

        # Identify the partition for each topic, and group them by broker.
        brokers = defaultdict(dict)
        for topic, keys in topics.iteritems():
            for key, messages in keys.iteritems():
                partition = self.partitioner(topic.partitions, key)
                brokers[partition.broker][partition] = data

        # Construct and send the multiproduce requests to each broker.
        for broker, partitions in brokers.iteritems():
            request = []
            for partition, messages in partitions.iteritems():
                request.append((partition.topic.name, partition.number, messages))
            broker.client.multiproduce(request)

        self.pending = []
