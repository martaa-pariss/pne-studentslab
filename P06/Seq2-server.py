from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import os

PORT = 8080

seq_list = ["ACGT", "CATG", "GATC", "TAGC", "AAAA"]

def load_html(file):
    with open(f"html/{file}", "r") as f:
        return f.read()

def complementary(seq):
    comp = ""
    for b in seq:
        if b == "A":
            comp += "T"
        elif b == "T":
            comp += "A"
        elif b == "C":
            comp += "G"
        elif b == "G":
            comp += "C"
    return comp


def reverse(seq):
    return seq[::-1]


def seq_info(seq):
    total = len(seq)
    result = f"<p>Sequence: {seq}</p>"
    result += f"<p>Total length: {total}</p>"

    for base in "ACGT":
        count = seq.count(base)
        perc = (count / total) * 100
        result += f"<p>{base}: {count} ({perc:.1f}%)</p>"

    return result


def read_fasta(filename):
    seq = ""
    with open(filename) as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip()
    return seq

#clase para el servidor
class SeqServer(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urlparse.urlparse(self.path)
        path = parsed.path
        params = urlparse.parse_qs(parsed.query)
        if path == "/":
            html = load_html("index.html")
        elif path == "/ping":
            html = "<h1>Server is alive</h1><a href='/'>Main page</a>"
        elif path == "/get":
            n = int(params.get("n", [0])[0])
            if 0 <= n <= 4:
                seq = seq_list[n]
                html = load_html("get.html").replace("{{sequence}}", seq)
            else:
                html = load_html("error.html")
        elif path == "/gene":
            name = params.get("name", [""])[0]

            genes = {
                "ADA": "sequences/ADA.file",
                "FRAT1": "sequences/FRAT1.file",
                "FXN": "sequences/FXN.file",
                "U5": "sequences/U5.file",
                "RNU6_269P": "sequences/RNU6_269P.file"
            }

            if name in genes:
                seq = read_fasta(genes[name])
                html = load_html("gene.html").replace("{{gene}}", seq)
            else:
                html = load_html("error.html")
        elif path == "/operation":
            seq = params.get("seq", [""])[0]
            op = params.get("op", [""])[0]

            if op == "info":
                html = load_html("operation.html").replace("{{result}}", seq_info(seq))
            elif op == "comp":
                html = load_html("operation.html").replace("{{result}}", complementary(seq))
            elif op == "rev":
                html = load_html("operation.html").replace("{{result}}", reverse(seq))
            else:
                html = load_html("error.html")
        else:
            html = load_html("error.html")
        #final
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


server = HTTPServer(("", PORT), SeqServer)
print("Server running...")
server.serve_forever()