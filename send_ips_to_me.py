#!/usr/bin/env python
import os
import sys
import time
import requests

HOST = "ip.loggerhead.me"
PORT = 8000
INTERVAL = 60


def get_ips():
    CMD = '''#!/bin/sh
    re="\d+\.\d+\.\d+\.\d+"
    ips=$(ifconfig | egrep $re | egrep -o "inet $re" | sed -E "s/(inet|127\.0\.0\.1)//g")

    for ip in $ips
    do
        echo $ip
    done'''

    return os.popen(CMD).read().split()

def get_users():
    FILTER = "_|#|nobody|daemon|bin|sys|sync|games|man|lp|mail|news|uucp|proxy|www-data|backup|list|irc|gnats|libuuid|syslog|messagebus|landscape|sshd|colord|redis|hduser|hadoop|Guest|macports"

    if sys.platform == "linux" or sys.platform == "linux2":
        CMD = 'cut -d: -f1 /etc/passwd | egrep -v "%s"' % FILTER
    elif sys.platform == "darwin":
        CMD = 'dscl . list /Users | egrep -v "%s"' % FILTER
    return os.popen(CMD).read().split()

def main():
    URL = "http://%s:%d" % (HOST, PORT)

    users = get_users()
    data = {'Users': users}

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
    main()
except KeyboardInterrupt:
    pass
