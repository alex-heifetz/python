#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess

res = str(subprocess.Popen('w', shell=True, stdout=subprocess.PIPE).communicate())
res = res.replace('\\n', "\n")
res = res.split("\n")

ips = []
for string in res:
    ip = re.search(r'(\d{1,3}.){3}\d{1,3}', string)
    if ip:
        ips.append(ip.group(0))

m = set(ips)
ips = []
for ip in m:
    subprocess.call("notify-send " + ip, shell=True)
