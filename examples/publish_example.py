from rainbow import register, publish, run


@register
def pub():
    publish('event', 'data')

run(host='0.0.0.0')
