import time

from fairground.client import create_process


count = 1
while True:
    command = 'sleep {0}'.format(count)
    create_process(command)
    count += 1
    time.sleep(1)
client.stop
