# Rainbow protocol

## Functions

### Description

When '_functions' method is requested by JSON-RPC, the result is a list of functions. Each function is defined by:

 * name: String
 * doc: String | Null
 * args: Object | Null
   * type: Number | String | Boolean | Array | Object | Null
   * value

#### Example

```python
@register
def test0():
    "Does nothing"
    pass

@register
def test1(a=0, b=0.0):
    """Add two elements"""
    return a + b

@register
def test2(a='', b=True):
    return '{0} {1}'.format(a, b)

@register
def test3(l=[1, False, {'item': 12}]):
    for i in l:
        print(i)
```

Generates

```javascript
[
   {
      "name": "test0",
      "doc": "Does nothing",
      "args": null
   },
   {
      "name": "test1",
      "doc": "Add two elements",
      "args": {
         "a": {
            "type": "Number",
            "value": 0
         },
         "b": {
            "type": "Number",
            "value": 0.0
         }
      }
   },
   {
      "name": "test2",
      "doc": null,
      "args": {
         "a": {
            "type": "String",
            "value": ""
         },
         "b": {
            "type": "Boolean",
            "value": true
         }
      }
   },
   {
      "name": "test3",
      "doc": null,
      "args": {
         "l": {
            "type": "Array",
            "value": [
               {
                  "type": "Number",
                  "value": 1
               },
               {
                  "type": "Boolean",
                  "value": false
               },
               {
                  "type": "Object",
                  "value": {
                     "item": {
                        "type": "Number",
                        "value": 12
                     }
                  }
               }
            ]
         }
      }
   }
]
```

### JSON-RPC

A Remote Procedure Call based on JSON is implemented: http://www.jsonrpc.org/specification

## Events

When 'publish' method is called in Python, an event is sent to all connected clients.

```python
publish('event.progress', 78.9)
```

Sends

```javascript
{
   "time": "2015-11-23T17:29:18.634255",
   "event": "event.progress",
   "data": 78.9
}
```
