from rainbow import register, publish, run


@register
def add(a=0, b=1.2, c=False, d={"item": True}, l=[1, 2, 3]):
    """Add a + b"""
    publish('event.add', '{0} + {1}'.format(a, b))
    return a + b


@register
def sub(a=0, b=3, text="text"):
    """Subtract a - b"""
    publish('event.sub', '{0} - {1}'.format(a, b))
    return a - b

run(host='0.0.0.0', avahi=True, webserver=True)  # sudo required
