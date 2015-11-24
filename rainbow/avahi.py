# -*- coding: utf-8 -*-
# This file is part of the Rainbow Project

__author__ = 'Jesús Arroyo Torrens'
__email__ = 'jesus.arroyo@bq.com'
__copyright__ = 'Copyright (c) 2015 Mundo Reader S.L.'
__license__ = 'GPLv2'


def run():
    _service = None
    name = 'avahi-daemon'
    try:
        import time
        import psutil
        import subprocess
        # Stop daemon if running
        subprocess.Popen(['service', name, 'stop'])
        time.sleep(0.5)
        # Start daemon
        subp = subprocess.Popen([name],
                                shell=False,
                                stdin=None,
                                stdout=None,
                                stderr=None,
                                close_fds=True)
        _service = psutil.Process(subp.pid)
    except:
        pass
    return _service


def kill(_service=None):
    if _service:
        _service.kill()
