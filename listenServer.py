#!/usr/bin/env python

import sys
import urlparse
import SocketServer
import SimpleHTTPServer


class HttpServer:
    class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def before(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            ip, port = self.request.getpeername()
            print self.headers
            print "Request IP: %s:%d" % (ip, port)

        def after(self):
            print '-' * 40

        def do_GET(self):
            self.before()
            self.after()

        def do_POST(self):
            self.before()
            self.print_post_data()
            self.after()

        def print_post_data(self):
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length).decode('utf-8')
            if not post_data:
                return

            pairs = urlparse.parse_qs(post_data)
            if pairs:
                for key, value in pairs.iteritems():
                    print "%s: %s" % (key, " ".join(value))
            else:
                print post_data


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
        print "Serving at: http://%s:%d" % (self.host, self.port)
        print '-' * 40

        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt as e:
            pass


if __name__ == "__main__":
    HttpServer().run()