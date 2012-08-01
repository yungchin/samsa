from kazoo.client import KazooClient
from samsa.cluster import Cluster
from samsa.metrics import MemoryBackedMetrics
from samsa.topics import Topic

kc = KazooClient()
kc.connect()

cluster = Cluster(kc)

def benchmark():
    topic = 'topic'

    messages = ['hello world', 'foobar']

    t = Topic(cluster, topic)
    t.publish(messages * 1000)

    consumer = t.subscribe('group2')
    consumer.instrumentor = MemoryBackedMetrics()


    print len(list(consumer))


    print consumer.instrumentor.export_histogram()


if __name__ == '__main__':
    benchmark()
