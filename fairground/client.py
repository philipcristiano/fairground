from fairground.connections import get_connected_zookeeper_client
import zookeeper

path = '/fairground/application/sleep'

def create_process(command):
    client = get_connected_zookeeper_client()
    try:
        client.create(path, command, makepath=True)
    except zookeeper.NodeExistsException:
        client.delete(path)
        client.create(path, command, makepath=True)
    client.stop()
