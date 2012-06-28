from pea import *
from fairground.client import create_process
from fairground.connections import get_connected_zookeeper_client
from fairground.proto_watcher import start_fairground, send_stop_message
from multiprocessing import Process
import psi.process


@step
def I_have_a_connection_to_zookeeper():
    world.zookeeper = get_connected_zookeeper_client()

@step
def A_fairground_is_running():
    world.fairground_process = start_fairground()

@step
def I_stop_the_fairground():
    send_stop_message()
    world.fairground_process.terminate()

@step
def I_add_a_process(process):
    create_process(process)

@step
def I_go_home():
        world.location = 'home'

@step
def There_is_a_running_process(process):
    import time
    time.sleep(2)
    for p in psi.process.ProcessTable().values():
        if process in p.command:
            return
    assert False

@step
def I_have_some_delicious(item):
        assert item in world.cart
        world.assertEquals(world.location, 'home')

# --------------------

class TestShopping(TestCase):
    def test_buying_some_peas(self):
        Given.I_have_a_connection_to_zookeeper()
        And.A_fairground_is_running()
        When.I_add_a_process('sleep 60')
        Then.There_is_a_running_process('sleep 60')

    def tearDown(self):
        Then.I_stop_the_fairground()
