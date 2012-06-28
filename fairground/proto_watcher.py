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

class Fairground(object):
    path = '/fairground/application/sleep'

    def __init__(self):
        self.arbiter = start_arbiter_process()

    def main(self):
        self.zookeeper_client = get_connected_zookeeper_client()
        try:
            print 'Watching znode'
            self.create_from_znode(self.path)
            self.arbiter.join()
        finally:
            self.zookeeper_client.stop()


    def watch_node(self, watched_event):
        print watched_event
        create_from_znode(path)

    def create_from_znode(self, path):
        print 'Getting znode'
        command, data = self.zookeeper_client.get(path, self.watch_node)
        print command, data
        create_watcher('sleep', command)
        print 'created watcher'

def main():
    fairground = Fairground()
    fairground.main()


def start_main_in_process():

    p = Process(target=main)
    p.start()
    return p

if __name__ == '__main__':
    main()

