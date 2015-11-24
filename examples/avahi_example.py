from rainbow import register, run


@register
def add(a=2, b=4.5):
    """Description: add"""
    1/0
    return a + b

run(host='0.0.0.0', avahi=True)  # sudo required
