from kazoo.client import KazooClient
import zookeeper
import time


client = KazooClient('33.33.33.10:2181')

client
client.connect()

print client.get_children('/')
print client.get_children('/zookeeper')

path = '/fairground/application/evo'
try:
    client.create(path, 'version=1', makepath=True, ephemeral=True)
except zookeeper.NodeExistsException:
    client.delete(path)
    print 'Node already exists, I deleted it!'
print client.get_children('/')
client.stop

time.sleep(120)
