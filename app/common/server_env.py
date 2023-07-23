import os


class ServerEnv(object):
    def __init__(self, gae_env, hostname):
        self.is_production = gae_env.startswith("standard")
        self.is_development = self.is_production is not True
        self.current = "production" if self.is_production else "development"
        protocol = "https" if self.is_production else "http"
        self.hostname = "{}://{}".format(protocol, hostname)


# See https://cloud.google.com/appengine/docs/standard/python3/runtime for
# the list of Python 3 runtime environment variables.
server_env = ServerEnv(
    os.getenv("GAE_ENV", ""),
    # Note - This is not used and will be replaced by different implementation
    # because in Python 3 runtime, there is no such environment variable,
    # the url/hostname needs to build manually, see more details here:
    # https://cloud.google.com/appengine/docs/standard/python/how-requests-are-routed
    os.getenv("DEFAULT_VERSION_HOSTNAME"),
)
