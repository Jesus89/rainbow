from rainbow import register, run


@register
def function(a, b, c=3.14, d='txt', e=False):
    return "Function: {0}{1}{2}{3}{4}".format(a, b, c, d, e)


@register
def test(a, b=3.14):
    return "Test: {0}{1}".format(a, b)


run(host='0.0.0.0')
