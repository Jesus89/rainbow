# Rainbow

[![License](http://img.shields.io/:license-gpl-blue.svg?style=flat)](http://opensource.org/licenses/GPL-2.0) [![Build Status](https://travis-ci.org/bqlabs/rainbow.svg)](https://travis-ci.org/bqlabs/rainbow)

Micro-framework for Python RPC+P&S communication over WebSockets
* Based on the [WAMP](http://wamp-proto.org/why/) protocol.
* Compatible with [JSON-RPC 2.0](http://www.jsonrpc.org/specification).
* Syntax inspired by [Bottle](https://github.com/bottlepy/bottle).

## Installation

```bash
sudo apt-get install python-dev libzmq-dev
pip install pyrainbow
```

## Example

Basic example

```python
from rainbow import register, run

@register('add')
def add(a, b):
    return a + b

run(host='0.0.0.0')
```

Publish example

```python
from rainbow import register, publish, run

@register('pub')
def pub():
    publish('event', 'data')

run(host='0.0.0.0')
```

Check more amazing [examples](https://github.com/bqlabs/rainbow/tree/develop/examples)!