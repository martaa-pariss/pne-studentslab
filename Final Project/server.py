import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PORT = 8080 #our port
socketserver.TCPServer.allow_reuse_address = True #This is for preventing the error: "Port already in use"

class TestHandler(http.server.BaseHTTPRequestHandler): # Class with our Handler. It's derived from BaseHTTPRequestHandler (our class inherits all his methods and properties)
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green') # Print the request line
        url_path = urlparse(self.path)
        path = url_path.path  # we get it from here
        params = parse_qs(url_path.query)
        try:
            if path == "/":
                self.send_html(self.main_page())
            elif path == "/listSpecies":
                self.list_species(params)
            elif path == "/karyotype":
                self.karyotype(params)
            elif path == "/chromosomeLength":
                self.chromosome_length(params)
        return

    def main_page(self):



Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
