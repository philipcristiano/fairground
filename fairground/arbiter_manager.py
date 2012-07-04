from multiprocessing import Process
import os.path

from circus.client import CircusClient
from circus import get_arbiter
from virtualenv import create_environment

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
    return os.path.join(home_dir, 'bin')



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
