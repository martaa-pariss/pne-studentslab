
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import requests
import json

PORT = 8080
ENSEMBL = "https://rest.ensembl.org"

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        params = urlparse.parse_qs(parsed_path.query)

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

    # ------------------------
    # BASIC
    # ------------------------

    def list_species(self, params):
        r = requests.get(f"{ENSEMBL}/info/species?content-type=application/json")
        data = r.json()
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
    # MEDIUM
    # ------------------------

    def gene_lookup(self, params):
        gene = params.get("gene", [None])[0]
        r = requests.get(f"{ENSEMBL}/xrefs/symbol/homo_sapiens/{gene}?content-type=application/json")
        data = r.json()

        if not data:
            return self.error_page("Gene not found")

        gene_id = data[0]["id"]
        self.send_html(f"<h1>ID: {gene_id}</h1>")

    def gene_seq(self, params):
        gene = params.get("gene", [None])[0]
        gene_id = self.get_gene_id(gene)

        r = requests.get(f"{ENSEMBL}/sequence/id/{gene_id}?content-type=application/json")
        seq = r.json()["seq"]

        self.send_html(f"<pre>{seq}</pre>")

    def gene_info(self, params):
        gene = params.get("gene", [None])[0]
        gene_id = self.get_gene_id(gene)

        r = requests.get(f"{ENSEMBL}/lookup/id/{gene_id}?content-type=application/json")
        data = r.json()

        html = f"""
        <h1>Gene Info</h1>
        <p>Start: {data['start']}</p>
        <p>End: {data['end']}</p>
        <p>Length: {data['end'] - data['start']}</p>
        <p>Chromosome: {data['seq_region_name']}</p>
        """

        self.send_html(html)

    def gene_calc(self, params):
        gene = params.get("gene", [None])[0]
        gene_id = self.get_gene_id(gene)

        r = requests.get(f"{ENSEMBL}/sequence/id/{gene_id}?content-type=application/json")
        seq = r.json()["seq"]

        length = len(seq)
        a = seq.count("A") / length * 100
        t = seq.count("T") / length * 100
        c = seq.count("C") / length * 100
        g = seq.count("G") / length * 100

        html = f"""
        <h1>Gene Calc</h1>
        <p>Length: {length}</p>
        <p>A: {a:.2f}%</p>
        <p>T: {t:.2f}%</p>
        <p>C: {c:.2f}%</p>
        <p>G: {g:.2f}%</p>
        """

        self.send_html(html)

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


# =============================
# client.py (ADVANCED)
# =============================

import requests

BASE = "http://localhost:8080"

r = requests.get(f"{BASE}/geneInfo?gene=FRAT1&json=1")
print(r.json())
