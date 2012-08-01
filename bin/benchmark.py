#!/usr/bin/env
"""
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

from kazoo.client import KazooClient
from samsa.cluster import Cluster
from samsa.metrics import MemoryBackedMetrics
from samsa.topics import Topic

kc = KazooClient()
kc.connect()

cluster = Cluster(kc)

def benchmark():
    topic = 'topic2'

    messages = ['hello world', 'foobar']

    t = Topic(cluster, topic)
    t.publish(messages * 10 ** 1)

    consumer = t.subscribe('group4')
    consumer.instrumentor = MemoryBackedMetrics()


    print len(list(consumer))

    print consumer.instrumentor.export_histogram()
    consumer.commit_offsets()


if __name__ == '__main__':
    benchmark()
