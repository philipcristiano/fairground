from kazoo.client import KazooClient
import zookeeper
import time


client = KazooClient('33.33.33.10:2181')

client
client.connect()

print client.get_children('/')
print client.get_children('/zookeeper')

path = '/fairground/application/evo'
while True:
    print client.get(path)
    time.sleep(1)
