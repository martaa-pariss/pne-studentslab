#############################CHAT##################################
import http.server
import socketserver
import urllib.parse

PORT = 8080

class EchoHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        # Página principal
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("html/form-e1.html", "r") as file:
                self.wfile.write(file.read().encode())

        # Echo
        elif self.path.startswith("/echo"):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            message = params.get("message", [""])[0]

            # Checkbox (mayúsculas)
            uppercase = "uppercase" in params

            if uppercase:
                message = message.upper()

            response = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Echo</title>
            </head>
            <body>
                <h1>Echo:</h1>
                <p>{message}</p>

                <br>
                <a href="/">Back to form</a>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(response.encode())

        # Error
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("html/error.html", "r") as file:
                self.wfile.write(file.read().encode())


with socketserver.TCPServer(("", PORT), EchoHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()


#PARA PROBAR EL SERVIDOR PONER ESTO EN EL BUSCADOR: http://localhost:8080