import json
import socket
import time

from circus import get_arbiter
from circus.process import Process
from pea import *
import psi.process
import zookeeper

from fairground.arbiter_manager import create_circus_client, ArbiterManager
from fairground.client import create_process
from fairground.connections import get_connected_zookeeper_client
from fairground.fair import start_main_in_process


class TestRunningASingleProcess(TestCase):
    def test_running_a_single_process(self):
        Given.I_have_removed_paths_from_zookeeper(['/fairground'])
        And.I_add_a_process('test_sleep', 'sleep 60')
        Given.I_have_a_circus_process_running_with_the_fairground_plugin()
        And.The_plugin_has_registered_the_node_with_zookeeper()

        And.I_assign_this_node_the_processes(['test_sleep'])
        Then.the_process_status_is_ok('test_sleep')
        And.There_is_a_running_process('sleep 60')

        Then.I_add_a_process('test_sleep', 'sleep 30')
        And.There_is_a_running_process('sleep 30')

        #And.I_assign_this_node_the_processes([])
        And.I_remove_the_process('test_sleep')
        And.The_process_is_not_in_the_arbiter('test_sleep')
        And.There_is_no_running_process('sleep 60')

    def tearDown(self):
        Then.I_stop_the_circus_daemon()

@step
def I_have_removed_paths_from_zookeeper(paths):
    I_have_a_connection_to_zookeeper()
    for path in paths:
        world.zookeeper.recursive_delete(path)

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
def The_plugin_has_registered_the_node_with_zookeeper():
    time.sleep(2)
    nodes = world.zookeeper.get_children('/fairground/nodes')
    world.node_name = socket.getfqdn()
    assert world.node_name in nodes

@step
def I_assign_this_node_the_processes(processes):
    path = '/fairground/process_assignments'
    world.zookeeper.ensure_path(path)
    assignment_path = path + '/' + world.node_name
    data = {'processes': processes}
    try:
        world.zookeeper.create(assignment_path, json.dumps(data))
    except zookeeper.NodeExistsException:
        world.zookeeper.set(assignment_path, json.dumps(data))

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
def I_remove_the_process(process_name):
    path = '/fairground/applications/{0}'.format(process_name)
    world.zookeeper.recursive_delete(path)

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
def The_process_is_not_in_the_arbiter(process):
    status_message = {
        "command": "list",
        "properties": {
            "name": process,
        }
    }

    for i in range(10):
        response = world.circus_client.call(status_message)
        if response['status'] == 'error' and response['errno'] == 3: # not found number
            return

        print response
        time.sleep(.5)

    assert False

@step
def There_is_a_running_process(process):
    for i in range(3):
        for p in psi.process.ProcessTable().values():
            if process in p.command:
                return
        time.sleep(1)
    assert False

@step
def There_is_no_running_process(process):
    for i in range(3):
        for p in psi.process.ProcessTable().values():
            if process in p.command:
                "still waiting"
                break
        return
        time.sleep(1)
    assert False

