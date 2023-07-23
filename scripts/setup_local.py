"""
This module sets up necessary local infrastructural services (e.g., PubSub,
Datastore, etc) for the local service environment.

Note that environment variables are injected from `docker-compose.test.yml`
"""

import os
import logging

log = logging.getLogger(__name__)


class ServerEnv(object):
    def __init__(self, software, hostname):
        self.is_production = software.startswith('Google App Engine/')
        self.is_development = self.is_production is not True
        self.current = 'production' if self.is_production else 'development'
        protocol = 'https' if self.is_production else 'http'
        self.hostname = '{}://{}'.format(protocol, hostname)


server_env = ServerEnv(
    os.getenv('SERVER_SOFTWARE', ''),
    os.getenv('PUBSUB_EMULATOR_HOST')
)

log.info("-----------------------------------------------------------------")
log.info(f"---------LOCAL SETUP ({os.getenv('SERVICE_NAME')}) PLACE HOLDER, DO NOTHING FOR NOW--------------")
log.info("-----------------------------------------------------------------")


def foo():
    pass

if __name__ == '__main__':
    foo()
