from Queue import Queue

from unittest2 import TestCase
from mock import Mock

from fairground.fair import Fairground, STOP_COMMAND, CHECK_APPLICATION_COMMAND, CHECK_EXISTING_APPLICATIONS
from fairground.arbiter_manager import ArbiterManager
from fairground.zookeeper_adaptor import ZookeeperAdaptor


class DescribeFairground(TestCase):

    queue_contents = []

    def setUp(self):
        self.am = Mock(name='arbiter_manager')
        self.zka = Mock(name='zookeeper_adaptor')
        self.zka.get_appliction_by_name = Mock(return_value=('COMMAND', 'DATA'))
        self.zka.get_applications = Mock(return_value=['APP1'])
        self.queue = Mock(Queue, name='queue')
        self.queue.get = Mock(side_effect=self.queue_contents + [(STOP_COMMAND, None)])

        self.fairground = Fairground(self.am, self.zka, self.queue)
        self.fairground.main()

    def should_stop_arbiter_manager(self):
        self.am.stop.assert_called_once_with()

    def should_stop_zookeeper_adaptor(self):
        self.zka.stop.assert_called_once_with()

    def should_add_command_to_check_existing_applications(self):
        self.queue.put.assert_any_call((CHECK_EXISTING_APPLICATIONS, None))


class DescribeFaigroundCheckingApplication(DescribeFairground):

    queue_contents = [(CHECK_APPLICATION_COMMAND, 'APPLICATION')]

    def setUp(self):
        super(DescribeFaigroundCheckingApplication, self).setUp()

    def should_add_application_to_arbiter(self):
        self.am.add_application.assert_called_once_with('APPLICATION', 'COMMAND')

    def should_have_callback_that_adds_application_check_to_the_queue(self):
        callback = self.zka.get_appliction_by_name.call_args[0][1]
        callback(Mock())

        self.queue.put.assert_called_with((CHECK_APPLICATION_COMMAND, 'APPLICATION'))


class DescribeFaigroundCheckingAllApplications(DescribeFairground):

    queue_contents = [(CHECK_EXISTING_APPLICATIONS, None)]

    def setUp(self):
        super(DescribeFaigroundCheckingAllApplications, self).setUp()

    def should_add_command_to_task_queue(self):
        self.queue.put.assert_called_with((CHECK_APPLICATION_COMMAND, 'APP1'))
