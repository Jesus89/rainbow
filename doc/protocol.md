# Rainbow protocol

## Functions

### Discovery

When '_functions' method is requested by JSON-RPC, result is the list of functions. Each function is defined by:

 * name: string
 * doc: string
 * args: dictionary

#### Example

 ```python
 @register('add')
 def add(a, b=5):
     """Add two elements"""
     return a + b

 @register('sub')
 def sub(a, b=10.2):
     """Subtract two elements"""
     return a - b
 ```

Generates

```javascript
[
   {
      "name":"add",
      "doc":"Add two elements",
      "args":{
         "a":null,
         "b":5
      }
   },
   {
      "name":"sub",
      "doc":"Subtract two elements",
      "args":{
         "a":null,
         "b":10.2
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
   "time":"2015-11-23T17:29:18.634255",
   "event":"event.progress",
   "data":78.9
}
```
