#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess


def global_status(action=None):
    actions = {
        'status': ['saved', 'poweroff', 'running'],
        'up': ['saved', 'poweroff'],
        'halt': ['running'],
        'suspend': ['running'],
        'reload': ['running'],
        'destroy': ['saved', 'poweroff', 'running']
    }

    res = str(subprocess.Popen('vagrant global-status --prune', shell=True, stdout=subprocess.PIPE).communicate())
    res = res.replace('\\n', "\n")
    res = res.split("\n")

    boxs = {}
    for string in res:
        box = re.search(r'^((\w|\d){7})\s+(\w+)\s+(\w+)\s+(\w+)\s+([a-z0-9-_\/]+)', string)
        if box:
            str_ = ('%(id)06s %(status)09s %(path)s' % {"id": box.group(1), "status": box.group(5),
                                                        "path": re.sub('\/home\/\w+', '~', box.group(6))})
            if box.group(5) in actions[action]:
                boxs.setdefault(box.group(1), box.group(5) + ' ' + re.sub('\/home\/\w+', '~', box.group(6)))
    return boxs
