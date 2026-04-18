import http.server
import socketserver
import termcolor
from pathlib import Path

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        # Si se pide "/" → index.html
        if self.path == "/":
            requested_file = "html/index.html"
        else:
            # Quitar la "/" inicial
            requested_file = self.path.lstrip("/")
        file_path = Path("html") / requested_file

        try:
            # Intentar abrir el archivo solicitado
            contents = file_path.read_text(encoding="utf-8")
            self.send_response(200)

        except FileNotFoundError:
            # Si no existe → cargar error.html
            error_path = Path("html") / "error.html"
            contents = error_path.read_text(encoding="utf-8")
            self.send_response(404)

        # Enviar cabeceras
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))
        self.end_headers()

        # Enviar contenido
        self.wfile.write(contents.encode())

        return


Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()