import http.server
import socketserver
import termcolor
PORT = 8080
socketserver.TCPServer.allow_reuse_address = True
class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(contents.encode()))
        self.end_headers()
        self.wfile.write(contents.encode())
        return
Handler = TestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
