from rainbow import register, run


@register
def test0():
    "Does nothing"
    pass


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

run(host='0.0.0.0')
