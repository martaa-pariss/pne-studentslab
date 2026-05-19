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

        # for json mpty dictionary
        datos_compartidos = {}
        # Limpiamos los parámetros por si viene el json=1 mezclado con tus variables
        params_limpios = params.replace("&json=1", "").replace("json=1&", "").replace("json=1", "")

        #CASO 1: Página principal
        if resource == "/" or resource == "":
            contents = Path('html/index.html').read_text()

        #CASO 2: Lista de especies con limite o no
        elif resource == "/listSpecies":
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/info/species", headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                specie = data['species']   # Leemos los datos y los convertimos de "texto" a "lista de Python"
                if "limit=" in params_limpios:
                    limite = int(params_limpios.split("=")[1])
                    specie = specie[:limite]
                # Creamos el trozo de HTML con los nombres
                list_html = ""
                for e in specie:
                    list_html += "<li>" + e['display_name'] + "</li>"

                # for json
                datos_compartidos = {"species": [e['display_name'] for e in specie]}

                # Cargamos la plantilla y cambiamos el "hueco" por nuestra lista
                page = Path('html/listSpecies.html').read_text()
                contents = page.replace("{{list}}", list_html)
            else:
                contents = "Error al conectar con Ensembl"
                error_code = 500

        #CASO 3: Cariotipo
        elif resource == "/karyotype":
            specie = params_limpios.split("=")[1] # Sacamos el nombre de la especie del parámetro (ej: species=human)
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/info/assembly/" + specie, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                chromosome = ", ".join(data['karyotype'])  # El cariotipo es una lista de nombres de cromosomas

                # for json
                datos_compartidos = {"species": specie, "karyotype": data['karyotype']}

                page = Path('html/karyotype.html').read_text()
                contents = page.replace("{{species}}", specie).replace("{{chromos}}", chromosome)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Specie not found")
                error_code = 404

        #CASO 4: Longitud del cromosoma
        elif resource == "/chromosomeLength":
            parts = params_limpios.split("&")
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

                # for json
                datos_compartidos = {"species": specie, "chromosome": chromosome, "length": long}

                page = Path('html/chromosomeLength.html').read_text()
                contents = page.replace("{{species}}", specie).replace("{{chromo}}", chromosome).replace("{{length}}", long)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Error en los datos")
                error_code = 404

            #MEDIUM LEVEL#
        # CASO 5: /geneLookup (Obtener el ID ENSG de un nombre de gen)
        elif resource == "/geneLookup":
            gene_name = params_limpios.split("=")[1]
            # API: /lookup/symbol/homo_sapiens/NOMBRE_GEN
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                gene_id = data['id']  # Esto nos da el ENS

                # for json
                datos_compartidos = {"gene": gene_name, "id": gene_id}

                page = Path('html/geneLookup.html').read_text()
                contents = page.replace("{{gene}}", gene_name).replace("{{id}}", gene_id)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Gene not found")
                error_code = 404

        # CASO 6: /geneSeq (Obtener la secuencia de ADN dado el nombre)
        elif resource == "/geneSeq":
            gene_name = params_limpios.split("=")[1]
            # PASO 1: Buscar el ID (igual que en el caso anterior)
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

                # for json
                datos_compartidos = {"gene": gene_name, "sequence": seq_data['seq']}

                page = Path('html/geneSeq.html').read_text()
                contents = page.replace("{{gene}}", gene_name).replace("{{sequence}}", seq_data['seq'])
            else:
                contents = "Error obteniendo secuencia"
                error_code = 404

        # CASO 7: /geneInfo (Detalles del gen)
        elif resource == "/geneInfo":
            gene_name = params_limpios.split("=")[1]
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                page = Path('html/geneInfo.html').read_text()
                length = data['end'] - data['start'] # Calculamos la longitud restando final e inicio

                # for json
                datos_compartidos = {"id": data['id'], "chromosome": data['seq_region_name'], "start": data['start'], "end": data['end'], "length": length}

                contents = page.replace("{{id}}", data['id']) \
                    .replace("{{chromo}}", data['seq_region_name']) \
                    .replace("{{start}}", str(data['start'])) \
                    .replace("{{end}}", str(data['end'])) \
                    .replace("{{length}}", str(length))
            else:
                contents = "Gene info not found"
                error_code = 404

        #CASO 8: longitud y pocentaje de secuencias
        elif resource == "/geneCalc":
            gene_name = params_limpios.split("=")[1]
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

                # for json
                datos_compartidos = {"length": length, "percentages": seq_percent(full_seq)}

                page = Path('html/geneCalc.html').read_text()
                contents = page.replace("{{length}}", length).replace("{{percents}}", percents)
            else:
                contents = "Error obteniendo secuencia"
                error_code = 404

        # CASO 9: /geneList (Genes en región)
        elif resource == "/geneList":
            parts = params_limpios.split("&")
            chromo = ""
            start = ""
            end = ""
            for part in parts:
                if part.startswith("chromo="): chromo = part.split("=")[1]
                elif part.startswith("start="): start = part.split("=")[1]
                elif part.startswith("end="): end = part.split("=")[1]
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            ensembl_url = f"/overlap/region/homo_sapiens/{chromo}:{start}-{end}?feature=gene"
            conn.request("GET", ensembl_url, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                list_html = ""
                lista_nombres_pure = []
                for gene in data:
                    gene_name = gene.get('external_name', gene.get('id', 'Unknown'))
                    list_html += f"<li>{gene_name}</li>"
                    lista_nombres_pure.append(gene_name)
                if list_html == "":
                    list_html = "<li>genes not found in this region</li>"

                # for json
                datos_compartidos = {"chromosome": chromo, "start": start, "end": end, "genes": lista_nombres_pure}

                page = Path('html/geneList.html').read_text()
                contents = page.replace("{{chromo}}", chromo).replace("{{start}}", start).replace("{{end}}", end).replace("{{list}}", list_html)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}","region not found")
                error_code = 404

        #error max
        else:
            contents = Path('html/error.html').read_text().replace("{{message}}", "Página no encontrada")
            error_code = 404

        # --- AQUÍ TERMINA EL TRUCO (REESCRIBIMOS LA SALIDA SI PIDIERON JSON) ---
        if "json=1" in params:
            content_type = 'application/json'
            if error_code != 200:
                # Si error en, JSON devolverá mensaje error
                contents = json.dumps({"error": f"Error {error_code} processing the request"})
            else:
                # CONVERTIMOS EL DICCIONARIO VACIO DEL PRINCIPIO QUE RELLENAMOS EN LOS ELIFS A JSON TEXTO
                contents = json.dumps(datos_compartidos)

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