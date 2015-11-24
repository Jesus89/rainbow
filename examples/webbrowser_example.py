from rainbow import register, run


@register
def add(a=0, b=0):
    return a + b

run(host='0.0.0.0', webserver=True, webbrowser=True)
