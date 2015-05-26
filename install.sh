#!/bin/sh

if [[ -z $1 ]]; then
    chmod a+x send_ips_to_me.py
    cp send_ips_to_me.py /usr/local/bin

    platform=`uname`
    if [[ "$platform" == 'Linux' ]]; then
        cp send_ips_to_me.py /etc/init.d/
        ln -s /etc/init.d/send_ips_to_me.py /etc/rc.d/
    elif [[ "$platform" == 'Darwin' ]]; then
        cp me.to.ips.send.plist /Library/LaunchDaemons
    fi

    echo $platform
elif [[ "$1" = "run" ]] || [[ "$1" == "-r" ]]; then
    nohup send_ips_to_me.py &
else
    read -p "Remove send_ips_to_me? " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ../send_ips_to_me
    fi
fi