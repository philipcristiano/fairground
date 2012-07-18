import zookeeper

from fairground.connections import get_connected_zookeeper_client


class ProcessDoesNotExist(Exception):
    pass


class ZookeeperAdaptor(object):

    path = '/fairground/applications'
    node_path = '/fairground/nodes'

    def __init__(self):
        self._client = get_connected_zookeeper_client()
        self._client.ensure_path(self.path)
        self._client.ensure_path(self.node_path)

    def get_application_by_name(self, application_name, callback):
        path = self.path + '/' + application_name
        try:
            return self._client.get(path, callback)
        except zookeeper.NoNodeException:
            raise ProcessDoesNotExist


    def get_application_names(self):
        return self._client.get_children(self.path)

    def register_node(self, name):
        path = self.node_path + '/' + name
        try:
            self._client.create(path, 'Huh', ephemeral=True, makepath=True)
        except zookeeper.NodeExistsException:
            pass

    def stop(self):
        self._client.stop()
