from kazoo.client import KazooClient
import zookeeper
import time


client = KazooClient('33.33.33.10:2181')

client
client.connect()

print client.get_children('/')

path = '/fairground/application/evo'
command = 'sleep 60'
try:
    client.create(path, command, makepath=True)
except zookeeper.NodeExistsException:
    client.delete(path)
    client.create(path, command, makepath=True)
    print 'Node already exists, I remade it!'
client.stop
