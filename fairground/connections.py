
from kazoo.client import KazooClient
def get_connected_zookeeper_client():
    zookeeper_client = KazooClient('33.33.33.10:2181')

    zookeeper_client
    zookeeper_client.connect()

    return zookeeper_client
