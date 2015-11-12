import base64
from rainbow import register, run


@register('save_file')
def save_file(name, content):
    with open(name, 'w') as file_:
        file_.write(base64.b64decode(content))
        return "OK"

run(host='0.0.0.0')
