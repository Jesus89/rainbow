# Rainbow

[![License](http://img.shields.io/:license-gpl-blue.svg?style=flat)](http://opensource.org/licenses/GPL-2.0) [![Build Status](https://travis-ci.org/bqlabs/rainbow.svg)](https://travis-ci.org/bqlabs/rainbow)

```
Work in progress
```

Micro-framework for Python RPC+P&S communication over WebSockets

## Installation

```bash
python setup.py install
```

## Example

Basic Example

```
from rainbow import register, run

@register('add')
def add(a, b):
    return a + b

run(host='0.0.0.0', port=8080)
```

Threading example

```
import time
import threading
from rainbow import register, run

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
        time.sleep(0.1)

@register('stop')
def stop():
    global running
    running = False

run(host='0.0.0.0', port=8080)
```
