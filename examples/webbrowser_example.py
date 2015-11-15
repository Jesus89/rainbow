from rainbow import register, run


@register('add')
def add(a, b):
    return a + b

run(host='0.0.0.0', webserver=True, webbrowser=True)
