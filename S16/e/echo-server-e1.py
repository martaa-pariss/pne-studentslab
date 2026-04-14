###############################WIKI#######################################
import http.server
import socketserver
from pathlib import Path

import termcolor

# Define the Server's port
PORT = 8080


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # Open the form1.html file
        # Read the index from the file
        contents = Path('e/html/form-1.html').read_text()

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()


####################################CHAT######################################
import http.server
import socketserver
import urllib.parse

PORT = 8080

class EchoHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        # Ruta principal
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("html/form-e1.html", "r") as file:
                self.wfile.write(file.read().encode())

        # Ruta /echo
        elif self.path.startswith("/echo"):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            message = params.get("message", [""])[0]

            response = f"""
            <html>
            <body>
                <h1>Echo:</h1>
                <p>{message}</p>

                <a href="/">Back to form</a>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(response.encode())

        # Cualquier otra ruta → error
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("html/error.html", "r") as file:
                self.wfile.write(file.read().encode())


# Ejecutar servidor
with socketserver.TCPServer(("", PORT), EchoHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

#PARA PROBAR EL SERVIDOR PONEMOS ESTO EN EL NAVEGADOR: http://localhost:8080

