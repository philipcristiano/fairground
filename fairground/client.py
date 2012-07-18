import json

from fairground.connections import get_connected_zookeeper_client
import zookeeper


base_path = '/fairground/applications/'

def create_process(name, command):
    path = base_path + name
    client = get_connected_zookeeper_client()
    data = json.dumps({
        'command': command,
        'name': name,
    })

    try:
        client.create(path, data, makepath=True)
    except zookeeper.NodeExistsException:
        client.set(path, data)
    client.stop()
