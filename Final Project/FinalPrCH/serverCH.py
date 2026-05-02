import http.server
from urllib.parse import parse_qs, urlparse
import requests
import termcolor
import json

PORT = 8080
ENSEMBL = "https://rest.ensembl.org" #esto es la parte de ruta que van a tener todos, se van poniendo barritas / dsps

class MyHandler(http.server.BaseHTTPRequestHandler):

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

            elif path == "/geneLookup":
                self.gene_lookup(params)

            elif path == "/geneSeq":
                self.gene_seq(params)

            elif path == "/geneInfo":
                self.gene_info(params)

            elif path == "/geneCalc":
                self.gene_calc(params)

            else:
                self.error_page("Endpoint not found")

        except Exception as e:
            self.error_page(str(e))

#first part (up to 6)
    def list_species(self, params):
        need = requests.get(f"{ENSEMBL}/info/species?content-type=application/json")
        data = need.json()
        species = [s["name"] for s in data["species"]]

        if "limit" in params:
            species = species[:int(params["limit"][0])]

        html = "<h1>Species</h1><ul>"
        for s in species:
            html += f"<li>{s}</li>"
        html += "</ul>"

        self.send_html(html)

    def karyotype(self, params):
        species = params.get("species", [None])[0]
        if not species:
            return self.error_page("Missing species")

        r = requests.get(f"{ENSEMBL}/info/assembly/{species}?content-type=application/json")
        data = r.json()

        chromosomes = data.get("karyotype", [])
        html = "<h1>Karyotype</h1><ul>"
        for c in chromosomes:
            html += f"<li>{c}</li>"
        html += "</ul>"

        self.send_html(html)

    def chromosome_length(self, params):
        species = params.get("species", [None])[0]
        chromo = params.get("chromo", [None])[0]

        r = requests.get(f"{ENSEMBL}/info/assembly/{species}?content-type=application/json")
        data = r.json()

        for region in data["top_level_region"]:
            if region["name"] == chromo:
                return self.send_html(f"<h1>Length: {region['length']}</h1>")

        self.error_page("Chromosome not found")


    # ------------------------
    # HELPERS
    # ------------------------

    def get_gene_id(self, gene):
        r = requests.get(f"{ENSEMBL}/xrefs/symbol/homo_sapiens/{gene}?content-type=application/json")
        data = r.json()
        return data[0]["id"]

    def main_page(self):
        return """
        <h1>Genome App</h1>
        <form action='/listSpecies'>Limit: <input name='limit'><input type='submit'></form>
        <form action='/karyotype'>Species: <input name='species'><input type='submit'></form>
        <form action='/chromosomeLength'>Species: <input name='species'> Chromo: <input name='chromo'><input type='submit'></form>
        <form action='/geneLookup'>Gene: <input name='gene'><input type='submit'></form>
        <form action='/geneSeq'>Gene: <input name='gene'><input type='submit'></form>
        <form action='/geneInfo'>Gene: <input name='gene'><input type='submit'></form>
        <form action='/geneCalc'>Gene: <input name='gene'><input type='submit'></form>
        """

    def send_html(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode())

    def error_page(self, msg):
        self.send_html(f"<h1>Error</h1><p>{msg}</p>")


if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), MyHandler)
    print(f"Server running on port {PORT}")
    server.serve_forever()

