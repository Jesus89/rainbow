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

```
from rainbow import register, run

@register('add')
def subtract(a, b):
    return a + b

run(host='0.0.0.0', port=8080)
```
