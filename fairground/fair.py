import time
from multiprocessing import Process, Queue

from fairground.arbiter_manager import ArbiterManager, create_circus_client
from fairground.zookeeper_adaptor import ZookeeperAdaptor
import zookeeper

STOP_COMMAND = 'STOP'
CHECK_APPLICATION_COMMAND = 'CHECK_APPLICATION'
CHECK_EXISTING_APPLICATIONS = 'CHECK_EXISTING_APPLICATIONS'


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
        task_queue.put((STOP_COMMAND, None))
        send_stop_message()
        p.terminate()
    return stop_function


def send_stop_message():
    circus_client = create_circus_client()
    circus_client.call({'command': 'quit'})


class Fairground(object):

    def __init__(self, arbiter_manager, zookeeper_adaptor, task_queue):
        self.arbiter_manager = arbiter_manager
        self.zookeeper_adaptor = zookeeper_adaptor
        self.task_queue = task_queue
        self._continue = True
        self.task_queue.put((CHECK_EXISTING_APPLICATIONS, None))

    def main(self):
        try:
            while self._continue:
                task = self.task_queue.get()
                self._process_task(task)
        finally:
            self.arbiter_manager.stop()
            self.zookeeper_adaptor.stop()

    def _process_task(self, task):
        if task[0] == STOP_COMMAND:
            self._continue = False
        elif task[0] == CHECK_APPLICATION_COMMAND:
            self.create_application_from_znode(task[1])
        elif task[0] == CHECK_EXISTING_APPLICATIONS:
            self.check_all_applications()

    def create_application_from_znode(self, name):
        def callback(watched_event):
            self.task_queue.put((CHECK_APPLICATION_COMMAND, name))
        command, data = self.zookeeper_adaptor.get_appliction_by_name(name, callback)
        self.arbiter_manager.add_application(name, command)

    def check_all_applications(self):
        for application in self.zookeeper_adaptor.get_applications():
            self.task_queue.put((CHECK_APPLICATION_COMMAND, application))


if __name__ == '__main__':
    main()

