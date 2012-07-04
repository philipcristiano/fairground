from fairground.connections import get_connected_zookeeper_client


class ZookeeperAdaptor(object):

    path = '/fairground/application/'

    def __init__(self):
        self._client = get_connected_zookeeper_client()

    def get_appliction_by_name(self, application_name, callback):
        path = self.path + application_name
        return self._client.get(path)

    def stop(self):
        self._client.stop()

    @classmethod
    def create_callback(func, *args, **kwargs):
        def callback(watched_event):
            func(*args, **kwargs)
        return callback
