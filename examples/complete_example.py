from rainbow import register, publish, run


@register('add')
def add(a, b):
    publish('event.add', '{0} + {1}'.format(a, b))
    return a + b

@register('sub')
def sub(a, b):
    publish('event.sub', '{0} - {1}'.format(a, b))
    return a - b

run(host='0.0.0.0', webserver=True, webbrowser=True)