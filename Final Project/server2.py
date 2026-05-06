import http.server
import socketserver
import http.client
import json
from pathlib import Path

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True # Evita que si reinicias el programa diga "Port already in use"

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self): #para GET el request, basicament, parteix el missatge pa llegir lo que es rsource i request i tal
        list_resource = self.path.split('?')
        resource = list_resource[0]
        params = ""
        if len(list_resource) > 1:
            params = list_resource[1]
        content_type = 'text/html'
        error_code = 200

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
                especies = data['species']   # Leemos los datos y los convertimos de "texto" a "lista de Python"
                if "limit=" in params:
                    limite = int(params.split("=")[1])
                    especies = especies[:limite]

                # Creamos el trozo de HTML con los nombres
                lista_html = ""
                for e in especies:
                    lista_html += "<li>" + e['display_name'] + "</li>"

                # Cargamos la plantilla y cambiamos el "hueco" por nuestra lista
                plantilla = Path('html/listSpecies.html').read_text()
                contents = plantilla.replace("{{list}}", lista_html)
            else:
                contents = "Error al conectar con Ensembl"
                error_code = 500

        #CASO 3: Cariotipo
        elif resource == "/karyotype":
            especie = params.split("=")[1] # Sacamos el nombre de la especie del parámetro (ej: species=human)

            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/info/assembly/" + especie, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                cromosomas = ", ".join(data['karyotype'])  # El cariotipo es una lista de nombres de cromosomas

                plantilla = Path('html/karyotype.html').read_text()
                contents = plantilla.replace("{{species}}", especie).replace("{{chromos}}", cromosomas)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Especie no encontrada")
                error_code = 404

        #CASO 4: Longitud del cromosoma
        elif resource == "/chromosomeLength":
            partes = params.split("&")
            especie = partes[0].split("=")[1]
            cromosoma = partes[1].split("=")[1]

            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/info/assembly/" + especie, headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                id = "No encontrado"
                # Buscamos en la lista de regiones la que coincida con el nombre del cromosoma
                for region in data['Transcript']:
                    if region['name'] == cromosoma:
                        id = str(region['length'])
                        break

                plantilla = Path('html/chromosomeLength.html').read_text()
                contents = plantilla.replace("{{species}}", especie).replace("{{chromo}}", cromosoma).replace(
                    "{{length}}", longitud)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Error en los datos")
                error_code = 404

            #MEDIUM LEVEL#
            # CASO 5: /geneLookup (Obtener el ID ENSG de un nombre de gen)
            elif resource == "/geneLookup":
            gene_name = params.split("=")[1]
            # API: /lookup/symbol/homo_sapiens/NOMBRE_GEN
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
            res = conn.getresponse()

            if res.status == 200:
                data = json.loads(res.read().decode())
                gene_id = data['id']  # Esto nos da el ENSG...
                plantilla = Path('html/geneLookup.html').read_text()
                contents = plantilla.replace("{{gene}}", gene_name).replace("{{id}}", gene_id)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Gene not found")
                error_code = 404

        # CASO 6: /geneSeq (Obtener la secuencia de ADN dado el nombre)
        elif resource == "/geneSeq":
        gene_name = params.split("=")[1]
        # PASO 1: Buscar el ID (igual que en el caso anterior)
        conn = http.client.HTTPSConnection("rest.ensembl.org")
        conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
        res = conn.getresponse()

        if res.status == 200:
            gene_id = json.loads(res.read().decode())['id']
            # PASO 2: Con el ID, pedir la secuencia
            # API: /sequence/id/ENSG...
            conn.request("GET", "/sequence/id/" + gene_id, headers={"Content-Type": "application/json"})
            res2 = conn.getresponse()
            seq_data = json.loads(res2.read().decode())

            plantilla = Path('html/geneSeq.html').read_text()
            contents = plantilla.replace("{{gene}}", gene_name).replace("{{sequence}}", seq_data['seq'])
        else:
            contents = "Error obteniendo secuencia"
            error_code = 404

    # CASO 7: /geneInfo (Detalles del gen)
    elif resource == "/geneInfo":
        gene_name = params.split("=")[1]
        conn = http.client.HTTPSConnection("rest.ensembl.org")
        conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name,
                     headers={"Content-Type": "application/json"})
        res = conn.getresponse()

        if res.status == 200:
            data = json.loads(res.read().decode())
            plantilla = Path('html/geneInfo.html').read_text()
            # Calculamos la longitud restando final e inicio
            length = data['end'] - data['start']

            contents = plantilla.replace("{{id}}", data['id']) \
                .replace("{{chromo}}", data['seq_region_name']) \
                .replace("{{start}}", str(data['start'])) \
                .replace("{{end}}", str(data['end'])) \
                .replace("{{length}}", str(length))
        else:
            contents = "Gene info not found"
            error_code = 404

        #error max
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
    print("Servidor funcionando en el puerto", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor parado por el usuario")
        httpd.server_close()