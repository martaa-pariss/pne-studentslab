import http.server
import socketserver
from pathlib import Path
import termcolor
from urllib.parse import urlparse, parse_qs  

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # MAIN PAGE (/)
        if path == "/":
            contents = """
            <html>
                <body>
                    <h1>Echo Server</h1>
                    <form action="/echo" method="get">
                        <input type="text" name="msg">
                        <input type="submit" value="Send">
                    </form>
                </body>
            </html>
            """

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(contents.encode()))
            self.end_headers()
            self.wfile.write(contents.encode())

        # ECHO (/echo)
        elif path == "/echo":
            params = parse_qs(parsed_path.query)
            message = params.get("msg", [""])[0]

            contents = f"""
            <html>
                <body>
                    <h1>Echo:</h1>
                    <p>{message}</p>
                    <a href="/">Back</a>
                </body>
            </html>
            """

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(contents.encode()))
            self.end_headers()
            self.wfile.write(contents.encode())

        # 🔹 ERROR PAGE
        else:
            contents = """
            <html>
                <body>
                    <h1>404 - Not Found</h1>
                    <a href="/">Back to form</a>
                </body>
            </html>
            """

            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
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