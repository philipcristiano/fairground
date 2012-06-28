import zookeeper
import time
from pprint import pprint
from circus import get_arbiter
from circus.client import CircusClient
from multiprocessing import Process
from fairground.connections import get_connected_zookeeper_client

def start_arbiter():
    arbiter = get_arbiter([])
    print 'starting arbiter'
    try:
        arbiter.start()
    finally:
        arbiter.stop()
        print 'Arbiter stopped :('

def start_arbiter_process():
    p = Process(target=start_arbiter)
    p.start()
    return p



def create_circus_client():
    return CircusClient()

def send_stop_message():
    circus_client = create_circus_client()
    circus_client.call({'command': 'quit'})

def create_watcher(name, command):
    circus_client = create_circus_client()
    message = {
        'command': 'add',
        'properties': {
            'cmd': command,
            'name': name,
            'args': [],
            'options': {},
            'start': True
        }
    }
    response = circus_client.call(message)
    if response['status'] == u'ok':
        print 'Added ', command, ' the first time!'
    else:
        remove_message = {
            'command': 'rm',
            'properties': {
                'name': name,
            }
        }
        circus_client.call(remove_message)
        circus_client.call(message)
        print 'Added ', command, ' the second time!'


path = '/fairground/application/sleep'
def watch_node(watched_event):
    print watched_event
    create_from_znode(path)

def create_from_znode(zookeeper_client, path):
    print 'Getting znode'
    command, data = zookeeper_client.get(path, watch_node)
    print command, data
    create_watcher('sleep', command)
    print 'created watcher'

def main():
    arbiter = start_arbiter_process()
    try:
        print 'Watching znode'
        zookeeper_client = get_connected_zookeeper_client()
        create_from_znode(zookeeper_client, path)
        arbiter.join()
    finally:
        zookeeper_client.stop()

def start_main_in_process():
    p = Process(target=main)
    p.start()
    return p

if __name__ == '__main__':
    main()

