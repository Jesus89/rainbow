import time
import threading
from rainbow import register, publish, run

running = False


@register('start')
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=_start).start()


def _start():
    global running
    while running:
        print "Hello, world!"
        publish('event.hello', "Hello, world!")
        time.sleep(3)


@register('stop')
def stop():
    global running
    running = False

run(host='0.0.0.0')
