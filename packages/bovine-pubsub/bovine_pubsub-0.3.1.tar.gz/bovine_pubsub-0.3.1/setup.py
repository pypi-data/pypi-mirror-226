# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bovine_pubsub']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=9.2.2,<10.0.0', 'bovine>=0.3.1,<0.4.0', 'quart-redis>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'bovine-pubsub',
    'version': '0.3.1',
    'description': 'A Quart thing to handle pubsub tasks in particular the event source',
    'long_description': '# bovine_pubsub\n\nbovine_pubsub is a simple wrapper to enable [server sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events) in bovine. These are used to communicate real time with clients without forcing them to use polling. If multiple workers are used with `bovine`, one needs to use Redis as the implementation with queues only works for a single process.\n\nStarting with `bovine-pubsub` support for server side clients is available using AMQP. See `examples/bovine_listen.py` for details.\n\n## Usage\n\nThe simplest usage example is given by\n\n```python\nfrom quart import Quart\nfrom bovine_pubsub import BovinePubSub\n\napp = Quart(__name__)\nBovinePubSub(app)\n```\n\nit adds the config variable `app.config["bovine_pub_sub"]` to the Quart application. By calling\n\n```python\nawait app.config["bovine_pub_sub"].send("channel:test", b"test")\n```\n\none sends the bytes `b"test"` to the channel `channel:test`. By calling\n\n```python\npub_sub.event_stream("channel:test")\n```\n\none receives an async iterator that can be used as server sent events.\n\n## Example usage\n\nA usage example is provided by `examples/basic_app.py`. By running\n\n```bash\npython examples/basic.app\n```\n\none can start a server that sends "test" 10 times a new socket is opened on `localhost:5000`. The above implementation will use the local queues. To use with Redis start\n\n```bash\nBOVINE_REDIS=redis://localhost:6379 python examples/basic_app.py \n```\n\nwith an appropriate value for the environment variable `BOVINE_REDIS`.\n\n## Running tests\n\nTesting redis can be done inside of the docker compose setup, e.g.\n\n```bash\ndocker compose up -d\ndocker compose run main /bin/sh\ncd bovine_pubsub\npoetry install\npoetry run pytest\nBOVINE_REDIS=redis://redis:6379 poetry run pytest\nBOVINE_AMQP=amqp://rabbitmq poetry run pytest\n```\n',
    'author': 'Helge',
    'author_email': 'helge.krueger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/bovine/bovine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
