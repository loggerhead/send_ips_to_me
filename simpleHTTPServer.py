#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import urlparse
import sys


class HttpServer:
    class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            print self.headers
            print

        def do_POST(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            print self.headers

            length = int(self.headers['Content-Length'])
            post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
            for key, value in post_data.iteritems():
                print "%s: %s" % (key, " ".join(value))
            print


    def __init__(self):
        self.port = 8000
        self.host = "0.0.0.0"

        if len(sys.argv) > 2:
            self.port = int(sys.argv[2])
            self.host = sys.argv[1]
        elif len(sys.argv) > 1:
            self.port = int(sys.argv[1])

        SocketServer.TCPServer.allow_reuse_address = True
        self.httpd = SocketServer.TCPServer((self.host, self.port), HttpServer.ServerHandler)

    def run(self):
        print "Serving at: http://%(interface)s:%(port)s" % dict(interface=self.host, port=self.port)
        print '-' * 40

        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt as e:
            pass

if __name__ == "__main__":
    HttpServer().run()