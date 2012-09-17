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
import os

from nose import collector


def run(*args, **kwargs):
    """
    Collects and runs tests using nose, ensuring that required directories
    exist for external dependencies.
    """
    vendor = os.path.join(os.path.dirname(__file__), '..', 'vendor')

    def configure_dependency_path(name):
        """
        Configures dependency paths to their defaults if they are not set by
        environment variables, and ensures that the referenced directories exist.
        """
        key = '%s_PATH' % name.upper()
        path = os.environ.setdefault(key, os.path.join(vendor, name))
        if not os.path.isdir(path):
            raise ValueError('The value of environment variable %s (%s) not a'
                'directory.' % (key, path))

    map(configure_dependency_path, ('kafka', 'zookeeper'))

    return collector(*args, **kwargs)
