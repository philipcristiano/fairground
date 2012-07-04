from fairground.connections import get_connected_zookeeper_client
import zookeeper

base_path = '/fairground/application/'

def create_process(name, command):
    path = base_path + name
    client = get_connected_zookeeper_client()
    try:
        client.create(path, command, makepath=True)
    except zookeeper.NodeExistsException:
        client.set(path, command)
    client.stop()
