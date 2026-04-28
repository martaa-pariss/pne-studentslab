import http.server
import socketserver
import http.client
import json
from twisted.internet.inotify import humanReadableMask

PORT = 8080


class GenomeHandler(http.server.BaseHTTPRequestHandler):

    def read_html(self, file_path):
        """Lee el contenido de un archivo HTML manualmente."""
        try:
            # Abrimos el archivo dentro de la carpeta html
            with open("html/" + file_path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return "<h1>Error: Fichero html/" + file_path + " no encontrado</h1>"

    def fetch_ensembl(self, endpoint):
        """Conecta con la API de Ensembl usando http.client."""
        context = http.client.HTTPSConnection("rest.ensembl.org")
        headers = {"Content-Type": "application/json"}
        context.request("GET", endpoint, headers=headers)

        response = context.getresponse()
        if response.status == 200:
            data = response.read().decode()
            return json.loads(data)
        else:
            return None

    def do_GET(self):
        # Separamos la ruta de los parámetros manualmente
        if "?" in self.path:
            path_solo, query = self.path.split("?", 1)
        else:
            path_solo = self.path
            query = ""

        # Diccionario para guardar los parámetros (especie, limit, etc.)
        params = {}
        if query:
            parts = query.split("&")
            for p in parts:
                key_value = p.split("=")
                if len(key_value) == 2:
                    params[key_value[0]] = key_value[1]

        # --- Lógica de Endpoints ---

        # 1) Página principal
        if path_solo == "/" or path_solo == "":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            content = self.read_html("index.html")
            self.wfile.write(content.encode())

        # 2) Lista de especies
        elif path_solo == "/listSpecies":
            limit = params.get("limit")
            data = self.fetch_ensembl("/info/species")

            if data:
                species_list = data['species']
                if limit:
                    species_list = species_list[:int(limit)]

                # Creamos el trozo de HTML con la lista
                html_items = ""
                for s in species_list:
                    html_items += "<li>" + s['display_name'] + "</li>"

                template = self.read_html("listSpecies.html")
                final_content = template.replace("{{list}}", html_items)

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(final_content.encode())
            else:
                self.send_error_page("Error conectando con Ensembl")

        # 3) Cariotipo
        elif path_solo == "/karyotype":
            species = params.get("species")
            data = self.fetch_ensembl("/info/assembly/" + species)

            if data and 'karyotype' in data:
                chromos = ", ".join(data['karyotype'])
                template = self.read_html("karyotype.html")
                final_content = template.replace("{{species}}", species).replace("{{chromos}}", chromos)

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(final_content.encode())
            else:
                self.send_error_page("Especie '" + str(species) + "' no encontrada")

        # 4) Longitud de cromosoma
        elif path_solo == "/chromosomeLength":
            species = params.get("species")
            chromo = params.get("chromo")
            data = self.fetch_ensembl("/info/assembly/" + species)

            length = None
            if data and 'top_level_region' in data:
                for region in data['top_level_region']:
                    if region['name'] == chromo:
                        length = region['length']
                        break

            if length:
                template = self.read_html("chromosomeLength.html")
                final_content = template.replace("{{species}}", species).replace("{{chromo}}", chromo).replace(
                    "{{length}}", str(length))

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(final_content.encode())
            else:
                self.send_error_page("Cromosoma o especie no encontrados")

        # Error 404 (Ruta no definida)
        else:
            self.send_error_page("Página no encontrada", 404)

    def send_error_page(self, message, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        template = self.read_html("error.html")
        self.wfile.write(template.replace("{{message}}", message).encode())


# Arrancar el servidor
with socketserver.TCPServer(("", PORT), GenomeHandler) as httpd:
    print("Servidor corriendo en el puerto", PORT)
    httpd.serve_forever()humanReadableMask()