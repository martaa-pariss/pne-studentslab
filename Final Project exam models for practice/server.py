import http.server
import socketserver
import http.client
import json
from pathlib import Path

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True # Evita que si reinicias el programa diga "Port already in use"
# defino aquí las funciones que necesite...
def seq_percent(seq):
    total = len(seq)
    bases = ['A', 'C', 'G', 'T']
    result = []
    for base in bases:
        count = seq.count(base)
        percentage = (count / total) * 100
        result.append(f"{base}: {count} ({percentage:.1f}%)")
    return result

#

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self): #para GET el request, basicament, parteix el missatge pa llegir lo que es rsource i request i tal
        list_resource = self.path.split('?')
        resource = list_resource[0]
        params = ""
        if len(list_resource) > 1:
            params = list_resource[1]
        content_type = 'text/html'
        error_code = 200

        # 1
        if resource == "/" or resource == "":
            contents = Path('html/index.html').read_text()

        #2: List
        elif resource == "/listSpecies":
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/info/species", headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                specie = data['species']   # Leemos los datos y los convertimos de "texto" a "lista de Python"
                if "limit=" in params:
                    limite = int(params.split("=")[1])
                    specie = specie[:limite]
                # Creamos el trozo de HTML con los nombres
                list_html = ""
                for e in specie:
                    list_html += "<li>" + e['display_name'] + "</li>"

                # Cargamos la plantilla y cambiamos el "hueco" por nuestra lista
                page = Path('html/listSpecies.html').read_text()
                contents = page.replace("{{list}}", list_html)
            else:
                contents = "Error al conectar con Ensembl"
                error_code = 500

        #3: karyo
        elif resource == "/karyotype":
            specie = params.split("=")[1] # Sacamos el nombre de la especie del parámetro (ej: species=human)
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/info/assembly/" + specie, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                chromosome = ", ".join(data['karyotype'])  # El cariotipo es una lista de nombres de cromosomas

                page = Path('html/karyotype.html').read_text()
                contents = page.replace("{{species}}", specie).replace("{{chromos}}", chromosome)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Specie not found")
                error_code = 404

        #4: Long
        elif resource == "/chromosomeLength":
            parts = params.split("&")
            specie = parts[0].split("=")[1]
            chromosome = parts[1].split("=")[1]

            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/info/assembly/" + specie, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                long = "not found"
                # Buscamos en la lista de regiones la que coincida con el nombre del cromosoma
                for region in data['top_level_region']:
                    if region['name'] == chromosome:
                        long = str(region['length'])
                        break

                page = Path('html/chromosomeLength.html').read_text()
                contents = page.replace("{{species}}", specie).replace("{{chromo}}", chromosome).replace("{{length}}", long)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Error en los datos")
                error_code = 404

            #MEDIUM LEVEL#
        #5: /geneLookup (ID)
        elif resource == "/geneLookup":
            gene_name = params.split("=")[1]
            # API: /lookup/symbol/homo_sapiens/NOMBRE_GEN
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                gene_id = data['id']  # Esto nos da el ENS
                page = Path('html/geneLookup.html').read_text()
                contents = page.replace("{{gene}}", gene_name).replace("{{id}}", gene_id)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Gene not found")
                error_code = 404

        # CASO 6: /geneSeq dado nombre
        elif resource == "/geneSeq":
            gene_name = params.split("=")[1] # para buscar n
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200: #AQUI TENGO QUE MIRAR PORQUE NO SE PORQUE TENGO Q OBTENER DOS RESPUESTAS DIFERENTES
                gene_id = json.loads(response.read().decode())['id']
                # PASO 2: Con el ID, pedir la secuencia
                # API: /sequence/id/ENSG...
                conn.request("GET", "/sequence/id/" + gene_id, headers={"Content-Type": "application/json"})
                response2 = conn.getresponse()
                seq_data = json.loads(response2.read().decode())

                page = Path('html/geneSeq.html').read_text()
                contents = page.replace("{{gene}}", gene_name).replace("{{sequence}}", seq_data['seq'])
            else:
                contents = "Error obteniendo secuencia"
                error_code = 404

        #7: /geneInfo
        elif resource == "/geneInfo":
            gene_name = params.split("=")[1]
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                page = Path('html/geneInfo.html').read_text()
                # Calculamos la longitud restando final e inicio
                length = data['end'] - data['start']

                contents = page.replace("{{id}}", data['id']) \
                    .replace("{{chromo}}", data['seq_region_name']) \
                    .replace("{{start}}", str(data['start'])) \
                    .replace("{{end}}", str(data['end'])) \
                    .replace("{{length}}", str(length))
            else:
                contents = "Gene info not found"
                error_code = 404

        #8: longitud porcentaje
        elif resource == "/geneCalc":
            gene_name = params.split("=")[1]
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
            response = conn.getresponse()
            if response.status == 200:
                gene_id = json.loads(response.read().decode())['id']
                conn.request("GET", "/sequence/id/" + gene_id, headers={"Content-Type": "application/json"})
                response2 = conn.getresponse()
                seq_data = json.loads(response2.read().decode())
                full_seq = seq_data['seq']
                length = str(len(full_seq))
                percents = str(seq_percent(full_seq))

                page = Path('html/geneCalc.html').read_text()
                contents = page.replace("{{length}}", length).replace("{{percents}}", percents)
            else:
                contents = "Error obteniendo secuencia"
                error_code = 404
        #9: /geneList (gnes en reg)
        elif resource == "/geneList":
            parts = params.split("&")
            chromo = ""
            start = ""
            end = ""
            for part in parts:
                if part.startswith("chromo="):
                    chromo = part.split("=")[1]
                elif part.startswith("start="):
                    start = part.split("=")[1]
                elif part.startswith("end="):
                    end = part.split("=")[1]
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            ensembl_url = f"/overlap/region/homo_sapiens/{chromo}:{start}-{end}?feature=gene"
            conn.request("GET", ensembl_url, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                list_html = ""
                for gene in data:
                    gene_name = gene.get('external_name', gene.get('id', 'Unknown'))
                    list_html += f"<li>{gene_name}</li>"
                if list_html == "": #po si no se encuentra nada
                    list_html = "<li>genes not found in this region</li>"
                page = Path('html/geneList.html').read_text()
                contents = page.replace("{{chromo}}", chromo).replace("{{start}}", start).replace("{{end}}", end).replace("{{list}}", list_html)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}","region not found")
                error_code = 404

        #error final
        else:
            contents = Path('html/error.html').read_text().replace("{{message}}", "Página no encontrada")
            error_code = 404
        self.send_response(error_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()
        self.wfile.write(str.encode(contents))


# programa handler
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("server running on port:", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by the user")
        httpd.server_close()