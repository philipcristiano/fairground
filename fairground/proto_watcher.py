import zookeeper
import time
from circus import get_arbiter
from circus.client import CircusClient
from multiprocessing import Process
from fairground.connections import get_connected_zookeeper_client
from virtualenv import create_environment
import os.path

BASE_DIR = './application_venvs'

def create_virtualenv(path, package):
    home_dir = os.path.join(BASE_DIR, path)

    create_environment(
        home_dir,
        site_packages=False,
        clear=False,
        unzip_setuptools=False,
        use_distribute=True,
        prompt=None,
        search_dirs=None,
        never_download=False
    )

def start_arbiter():
    arbiter = get_arbiter([])
    try:
        arbiter.start()
    finally:
        arbiter.stop()

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
    create_virtualenv(name, name)
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
    if response['status'] != u'ok':
        remove_message = {
            'command': 'rm',
            'properties': {
                'name': name,
            }
        }
        circus_client.call(remove_message)
        circus_client.call(message)

class Fairground(object):
    path = '/fairground/application/sleep'

    def __init__(self):
        self.arbiter = start_arbiter_process()

    def main(self):
        self.zookeeper_client = get_connected_zookeeper_client()
        try:
            self.create_from_znode(self.path)
            self.arbiter.join()
        finally:
            self.zookeeper_client.stop()


    def watch_node(self, watched_event):
        create_from_znode(path)

    def create_from_znode(self, path):
        command, data = self.zookeeper_client.get(path, self.watch_node)
        create_watcher('sleep', command)

def main():
    fairground = Fairground()
    fairground.main()


def start_main_in_process():

    p = Process(target=main)
    p.start()
    return p

if __name__ == '__main__':
    main()

