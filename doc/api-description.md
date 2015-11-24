# API Description

In order to define functions' input and output parameters, they must be properly defined in Python.

## Ideas

### Default parameters

Input parameters can be defined using default values. Output type can not be defined.

```python
@register
def add(a=0, b=0):
    return a + b
```

### Custom docstring

Input and output parameters can be defined in docstring:

```python
@register
def add(a, b):
    """
    (int, int) -> int
    """
    return a + b
```

### Register decorator

Input and output parameters can be defined in 'register' decorator:

```python
@register(int, int, int)  # a, b, return
def add(a, b):
    return a + b
```

### Function annotations (only in Python 3)

For future Python 3 compatibility, function annotations may be used:

```python
@register
def add(a: int, b: int) -> int:
    return a + b
```
