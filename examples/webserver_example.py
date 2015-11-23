from rainbow import register, run


@register
def add(a, b):
    return a + b

run(host='0.0.0.0', webserver=True)
