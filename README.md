#Install
Change `HOST` in `send_ips_to_me.py` to you server host.

```shell
chmod a+x send_ips_to_me.py
cp send_ips_to_me.py /usr/local/bin
```

####OS X
```shell
mv send.ips.to.me.plist /Library/LaunchDaemons
```

####Linux
```shell
# NOTE: Maybe not work
cp send_ips_to_me.py /etc/init.d/
ln -s /etc/init.d/send_ips_to_me.py /etc/rc.d/
```

#Usage
execute `nohup send_ips_to_me.py &` or restart on your client and execute `python simpleHTTPServer.py` on your server.