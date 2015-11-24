![][rainbow]

[![License](http://img.shields.io/:license-gpl-blue.svg?style=flat)](http://opensource.org/licenses/GPL-2.0) [![Build Status](https://travis-ci.org/bqlabs/rainbow.svg)](https://travis-ci.org/bqlabs/rainbow)

Micro-framework for Python RPC+Pub/Sub communication over WebSockets
* Based on the [WAMP](http://wamp-proto.org/why/) protocol.
* Compatible with [JSON-RPC 2.0](http://www.jsonrpc.org/specification).
* JSON Events using the [Publish/Subscribe pattern](http://rfc.zeromq.org/spec:29).
* Syntax inspired by [Bottle](https://github.com/bottlepy/bottle).

## Installation

```bash
sudo apt-get install python-dev libzmq-dev avahi-daemon

# Disable avahi on init
sudo update-rc.d -f avahi-daemon remove

sudo pip install pyrainbow
```

## Protocol

[Rainbow protocol](doc/protocol.md)

## Description

[API description](doc/api-description.md)

## Example

Basic example

```python
from rainbow import register, run

@register
def add(a=0, b=0):
    return a + b

run(host='0.0.0.0')
```

Publish example

```python
from rainbow import register, publish, run

@register
def pub():
    publish('event', 'data')

run(host='0.0.0.0')
```

Check more amazing [examples](https://github.com/bqlabs/rainbow/tree/develop/examples)!

[rainbow]: doc/images/rainbow.png
