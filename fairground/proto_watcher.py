import zookeeper
import time
from multiprocessing import Process, Queue
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

    def __init__(self, arbiter_manager, zookeeper_adaptor, task_queue):
        self.arbiter_manager = arbiter_manager
        self.zookeeper_adaptor = zookeeper_adaptor
        self.task_queue = task_queue

    def main(self):
        try:
            self.create_application_from_znode(self.path)
            import time
            time.sleep(10)
        finally:
            self.arbiter_manager.stop()
            self.zookeeper_adaptor.stop()

    def watch_node(self, watched_event):
        self.create_application_from_znode(path)

    def create_application_from_znode(self, path):
        callback = self.zookeeper_adaptor.create_callback(self.create_application_from_znode, path)
        command, data = self.zookeeper_adaptor.get_appliction_by_name('sleep', self.watch_node)
        self.arbiter_manager.add_application('test_process', command)


def main(task_queue):
    arbiter_manager = ArbiterManager()
    zka = ZookeeperAdaptor()
    fairground = Fairground(arbiter_manager, zka, task_queue)
    fairground.main()


def start_main_in_process():
    task_queue = Queue()
    p = Process(target=main, args=[task_queue])
    p.start()
    def stop_function():
        task_queue.put(('STOP', None))
        send_stop_message()
        p.terminate()
    return stop_function

if __name__ == '__main__':
    main()

