class Batch(object):
    def __init__(self, cluster):
        self.cluster = cluster
        self.pending = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.flush()

    def publish(self, topic, data, key=None):
        """
        Queues a message (or messages) to be published upon flushing this batch.
        """
        self.pending.append((topic, data, key))

    def flush(self):
        raise NotImplementedError
