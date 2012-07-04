from circus.client import CircusClient
from circus import get_arbiter
from multiprocessing import Process


def create_circus_client():
    return CircusClient(timeout=15)

class ArbiterManager(object):

    def __init__(self):
        self._arbiter = get_arbiter([], background=True)
        self._arbiter.start()
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

    def stop(self):
        self._arbiter.stop()

def start_arbiter():
    arbiter.start()
