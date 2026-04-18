###############################WIKI#######################################
import http.server
import socketserver
from pathlib import Path
import termcolor

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        try:
            contents = Path('html/form-e1.html').read_text()
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(str.encode(contents)))
            self.end_headers()
            # Send the response message
            self.wfile.write(str.encode(contents))
        except FileNotFoundError:
            print("we could not find the file")
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



