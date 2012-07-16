from Queue import Queue
import logging
import json

from circus.plugins import CircusPlugin

from fairground.zookeeper_adaptor import ZookeeperAdaptor


class FairgroundPlugin(CircusPlugin):

    def __init__(self, *args, **kwargs):
        super(FairgroundPlugin, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger('Fairground')
        self.logger.info('Fairground initializing')
        self.zka = ZookeeperAdaptor()
        self.notification_queue = Queue()
        self.logger.info('Fairground initialized')

    def initialize(self, *args, **kwargs):
        super(FairgroundPlugin, self).initialize(*args, **kwargs)
        self.start_application()

    def start_application(self):
        for application_name in self.zka.get_application_names():
            print application_name
            def application_callback(watched_event):
                self.notification_queue.put(('APP', application_name))
            (data, metadata) = self.zka.get_appliction_by_name(application_name, application_callback)
            application = json.loads(data)
            self.add_application(application)

    def handle_stop(self):
        self.zka.stop()

    def handle_recv(self, data):
        print data

    def add_application(self, application):
        properties = {
            'cmd': application['command'],
            'name': application['name'],
            'args': [],
            #'working_dir': cwd,
            'options': {},
            'start': True
        }
        response = self.call('add', **properties)
        print response
        return
        if response['status'] != u'ok':
            remove_message = {
                'command': 'rm',
                'properties': {
                    'name': application['name'],
                }
            }
            self.call('rm', name=application['name'])
            response = self.call('add', **properties)


