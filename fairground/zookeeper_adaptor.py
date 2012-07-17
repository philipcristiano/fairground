from fairground.connections import get_connected_zookeeper_client


class ZookeeperAdaptor(object):

    path = '/fairground/applications'

    def __init__(self):
        self._client = get_connected_zookeeper_client()

    def get_appliction_by_name(self, application_name, callback):
        path = self.path + '/' + application_name
        return self._client.get(path, callback)

    def get_application_names(self):
        return self._client.get_children(self.path)

    def stop(self):
        self._client.stop()
