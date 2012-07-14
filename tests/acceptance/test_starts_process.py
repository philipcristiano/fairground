from pea import *
from circus.process import Process
from circus import get_arbiter
from fairground.client import create_process
from fairground.connections import get_connected_zookeeper_client
from fairground.arbiter_manager import create_circus_client, ArbiterManager
from fairground.fair import start_main_in_process
import psi.process
import time


class TestRunningASingleProcess(TestCase):
    def test_running_a_single_process(self):
        Given.I_have_a_circus_process_running_with_the_fairground_plugin()
        # And.I_add_a_process('test_sleep', 'sleep 60')
        # Then.the_process_status_is_ok('test_sleep')
        # And.There_is_a_running_process('SimpleHTTPServer')
        # And.There_is_a_running_process('sleep 60')

    def tearDown(self):
        Then.I_stop_the_circus_daemon()

@step
def I_have_a_circus_process_running_with_the_fairground_plugin():
    plugins = [{'use': 'fairground.plugin.FairgroundPlugin'}]
    world.am = ArbiterManager(plugins=plugins)

    world.circus_client = create_circus_client()
    status = {'command': 'status'}
    assert world.circus_client.call(status)['status'] == 'ok'

@step
def I_stop_the_circus_daemon():
    world.am.stop()

@step
def I_start_the_fairground_plugin():
    pass


@step
def I_have_a_connection_to_zookeeper():
    world.zookeeper = get_connected_zookeeper_client()

@step
def I_stop_the_zookeeper_connection():
    world.zookeeper.stop()

@step
def I_have_a_circus_client():
    world.circus_client = create_circus_client()

@step
def A_fairground_is_running():
    world.fairground_stop_func = start_main_in_process()

@step
def I_stop_the_fairground():
    world.fairground_stop_func()

@step
def I_add_a_process(name, process):
    create_process(name, process)

@step
def the_process_status_is_ok(process):
    status_message = {
        "command": "list",
        "properties": {
            "name": process,
        }
    }
    for i in range(10):
        response = world.circus_client.call(status_message)
        if response['status'] == 'ok':
            return
        time.sleep(1)
    assert False

@step
def There_is_a_running_process(process):
    for p in psi.process.ProcessTable().values():
        if process in p.command:
            return
    assert False

