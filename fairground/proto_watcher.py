from kazoo.client import KazooClient
import zookeeper
import time
from circus import get_arbiter
from circus.client import CircusClient
from multiprocessing import Process

def start_arbiter():
    arbiter = get_arbiter([])
    print 'starting arbiter'
    try:
        arbiter.start()
    finally:
        arbiter.stop()

p = Process(target=start_arbiter)
p.start()

zookeeper_client = KazooClient('33.33.33.10:2181')

zookeeper_client
zookeeper_client.connect()

print zookeeper_client.get_children('/')
print zookeeper_client.get_children('/zookeeper')

circus_client = CircusClient()

def create_watcher(command):
    message = {
        'command': 'add',
        'properties': {
            'cmd': command,
            'name': 'sleep',
            'args': [],
            'options': {},
            'start': True
        }
    }
    print circus_client.call(message)

path = '/fairground/application/evo'
try:
    while True:
        command, data = zookeeper_client.get(path)
        print command, data
        create_watcher(command)
        time.sleep(30)
finally:
    zookeeper_client.stop()
