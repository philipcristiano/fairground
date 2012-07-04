from circus.client import CircusClient
from circus import get_arbiter
from multiprocessing import Process


def create_circus_client():
    return CircusClient(timeout=15)

class ArbiterManager(object):

    def __init__(self):
        self._arbiter_process = start_arbiter_process()
        self._client = create_circus_client()

    def add_application(self, name, command):
        #cwd = create_virtualenv(name, name)
        message = {
            'command': 'add',
            'properties': {
                'cmd': command,
                'name': name,
                'args': [],
                #'working_dir': cwd,
                'options': {},
                'start': True
            }
        }
        response = self._client.call(message)
        if response['status'] != u'ok':
            remove_message = {
                'command': 'rm',
                'properties': {
                    'name': name,
                }
            }
            self._client.call(remove_message)
            self._client.call(message)

    def join(self):
        self._arbiter_process.join()

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
