import http.server
import socketserver
import termcolor

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        # Determinar qué archivo servir
        if self.path == "/" or self.path == "/index.html":
            filename = "index.html"
            self.send_response(200)
        else:
            filename = "error.html"
            self.send_response(404)

        try:
            # Abrir el archivo HTML
            with open(filename, "r", encoding="utf-8") as f:
                contents = f.read()

            # Enviar cabeceras
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(contents.encode()))
            self.end_headers()

            # Enviar contenido
            self.wfile.write(contents.encode())

        except FileNotFoundError:
            # Por si el archivo no existe
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

        return


Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()