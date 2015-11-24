from rainbow import register, publish, run


@register
def pub():
    publish('event', 1234)

run(host='0.0.0.0')
