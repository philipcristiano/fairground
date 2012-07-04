from pea import *
from fairground.client import create_process
from fairground.connections import get_connected_zookeeper_client
from fairground.arbiter_manager import create_circus_client
from fairground.fair import start_main_in_process
from multiprocessing import Process
import psi.process
import time


class TestRunningASingleProcess(TestCase):
    def test_running_a_single_process(self):
        Given.I_have_a_connection_to_zookeeper()
        And.A_fairground_is_running()
        And.I_have_a_circus_client()

        When.I_add_a_process('test_process', 'python -m SimpleHTTPServer')
        And.I_add_a_process('test_sleep', 'sleep 60')

        Then.I_check_the_process_status('test_process')
        And.I_check_the_process_status('test_sleep')
        And.There_is_a_running_process('SimpleHTTPServer')
        And.There_is_a_running_process('sleep 60')

    def tearDown(self):
        Then.I_stop_the_fairground()
        Then.I_stop_the_zookeeper_connection()


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
def I_check_the_process_status(process):
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

