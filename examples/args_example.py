from rainbow import register, publish, run


@register
def test0():
    "Publish an event"
    publish('event', {'v': 3.14})


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
    return "OK"

run(host='0.0.0.0', webserver=True, webbrowser=True)
