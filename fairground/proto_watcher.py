import zookeeper
import time
from multiprocessing import Process
from fairground.arbiter_manager import ArbiterManager, create_circus_client
from fairground.zookeeper_adaptor import ZookeeperAdaptor
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
    return os.path.join(home_dir, 'bin')



def send_stop_message():
    circus_client = create_circus_client()
    circus_client.call({'command': 'quit'})


class Fairground(object):
    path = '/fairground/application/sleep'

    def __init__(self):
        self.arbiter_manager = ArbiterManager()

    def main(self):
        self.zookeeper_adaptor = ZookeeperAdaptor()
        try:
            self.create_application_from_znode(self.path)
            import time
            time.sleep(10)
        finally:
            self.arbiter_manager.stop()
            self.zookeeper_adaptor.stop()
            print self.zookeeper_adaptor._client.state

    def watch_node(self, watched_event):
        self.create_application_from_znode(path)

    def create_application_from_znode(self, path):
        callback = self.zookeeper_adaptor.create_callback(self.create_application_from_znode, path)
        command, data = self.zookeeper_adaptor.get_appliction_by_name('sleep', self.watch_node)
        self.arbiter_manager.add_application('test_process', command)


def main():
    fairground = Fairground()
    fairground.main()


def start_main_in_process():

    p = Process(target=main)
    p.start()
    return p

if __name__ == '__main__':
    main()

