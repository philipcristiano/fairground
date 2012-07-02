from pea import *
from fairground.client import create_process
from fairground.connections import get_connected_zookeeper_client
from fairground.proto_watcher import send_stop_message, create_circus_client, start_main_in_process
from multiprocessing import Process
import psi.process
import time


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
    world.fairground_process = start_main_in_process()

@step
def I_stop_the_fairground():
    send_stop_message()
    world.fairground_process.terminate()

@step
def I_add_a_process(process):
    create_process(process)

@step
def I_check_the_process_status(process):
    status_message = {
        "command": "list",
        "properties": {
            "name": process,
        }
    }
    for i in range(60):
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

@step
def I_have_some_delicious(item):
        assert item in world.cart
        world.assertEquals(world.location, 'home')

# --------------------

class TestRunningASingleProcess(TestCase):
    def test_running_a_single_process(self):
        Given.I_have_a_connection_to_zookeeper()
        And.A_fairground_is_running()
        And.I_have_a_circus_client()
        When.I_add_a_process('sleep 60')
        Then.I_check_the_process_status('sleep')
        And.There_is_a_running_process('sleep 60')

    def tearDown(self):
        Then.I_stop_the_fairground()
        Then.I_stop_the_zookeeper_connection()
