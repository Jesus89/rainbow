from rainbow import register, publish, run


@register
def add(a, b=2):
    publish('event.add', '{0} + {1}'.format(a, b))
    return a + b


@register
def sub(a, b=3):
    publish('event.sub', '{0} - {1}'.format(a, b))
    return a - b

run(host='0.0.0.0', webserver=True, webbrowser=True)
