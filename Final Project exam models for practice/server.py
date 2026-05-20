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










#####PRACTICA PARA EL EXAMEN######
        #A
        elif resource == "/geneType":
            gene_name = params.split("=")[1] # API: /lookup/symbol/homo_sapiens/NOMBRE_GEN
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name, headers={"Content-Type": "application/json"})
            response = conn.getresponse()
            if response.status == 200:
                data = json.loads(response.read().decode())
                biotype = data['biotype']
                strand = str(data['strand'])
                page = Path('html/geneType.html').read_text()
                contents = page.replace("{{gene}}", gene_name).replace("{{biotype}}", biotype).replace("{{strand}}", strand)
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Gene not found")
                error_code = 404

        #B
        elif resource == "/listSpecies2":
            parts = params.split("&")
            limit = int(parts[0].split("=")[1])
            division = parts[1].split("=")[1]

            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/info/species", headers={"Content-Type": "application/json"})
            response = conn.getresponse()
            if response.status == 200:
                data = json.loads(response.read().decode())
                species = data['species']   # Leemos los datos y los convertimos de "texto" a "lista de Python"
                list_html = ""
                for especie in species:
                    if especie['division'] == division:
                        list_html += "<li>" + especie['display_name'] + "</li>"
                        number = list_html.count("<li>")
                        if number == limit:
                            break

                # Cargamos la plantilla y cambiamos el "hueco" por nuestra lista
                page = Path('html/listSpecies2.html').read_text()
                contents = page.replace("{{list}}", list_html)
            else:
                contents = "Error al conectar con Ensembl"
                error_code = 500

        #C
        elif resource == "/geneCompLen":
            parts = params.split("&")
            gene1 = parts[0].split("=")[1]
            gene2 = parts[1].split("=")[1]
            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn2 = http.client.HTTPSConnection("rest.ensembl.org")
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene1, headers={"Content-Type": "application/json"})
            conn2.request("GET", "/lookup/symbol/homo_sapiens/" + gene2, headers={"Content-Type": "application/json"})
            response = conn.getresponse()
            response2 = conn2.getresponse()
            if response.status == 200:
                data = json.loads(response.read().decode())
                length1 = int(data['end'] - data['start'])
                if response2.status == 200:
                    data2 = json.loads(response2.read().decode())
                    length2 = int(data2['end'] - data2['start'])
                    if length1 > length2:
                        dif = length1 - length2
                        message = f"The first gene {gene1} is longer than the second {gene2}"
                    elif length1 < length2:
                        dif = length2 - length1
                        message = f"The second gene {gene2} is longer than the first {gene1}"
                    elif length1 == length2:
                        dif = 0
                        message = "both genes are the same length"

                    page = Path('html/geneCompLen.html').read_text()
                    contents = page.replace("{{message}}", message).replace("{{difference}}", str(dif))

            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Gene not found")
                error_code = 404

        #D
        elif resource == "/geneOverlapStats":
            gene_name = params.split("=")[1] #1.Troceamos los parámetros
            conn = http.client.HTTPSConnection("rest.ensembl.org") # Creamos las dos conexiones que vamos a necesitar
            conn2 = http.client.HTTPSConnection("rest.ensembl.org")


            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name,
                         headers={"Content-Type": "application/json"}) # Primera petición: Buscamos los datos básicos del gen
            response = conn.getresponse()

            if response.status == 200: # Primer IF
                data = json.loads(response.read().decode())
                # Guardamos las coordenadas y el ID del gen original
                chromo = data['seq_region_name']
                start = str(data['start'])
                end = str(data['end'])
                my_id = data['id']

                # Calculamos la longitud de nuestro gen
                my_length = int(data['end'] - data['start'])

                # Segunda petición: Buscamos qué solapa en ese cromosoma y coordenadas
                # Usamos la estructura de URL típica de Ensembl: /overlap/region/homo_sapiens/CROMOSOMA:INICIO-FIN?feature=gene
                conn2.request("GET",
                              "/overlap/region/homo_sapiens/" + chromo + ":" + start + "-" + end + "?feature=gene",
                              headers={"Content-Type": "application/json"})
                response2 = conn2.getresponse()

                # Segundo IF anidado a tu manera
                if response2.status == 200:
                    data2 = json.loads(response2.read().decode())  # Esto nos devuelve una lista de genes que solapan

                    # Inicializamos las variables para el examen: el contador y los datos del vecino más grande
                    overlap_count = 0
                    max_length = 0
                    max_name = "None"

                    # Recorremos la lista de genes que solapan con un bucle for (como en tu listSpecies)
                    for especie in data2:
                        # Muy importante: Comprobamos que el gen que está solapando NO sea nuestro propio gen
                        if especie['id'] != my_id:
                            overlap_count = overlap_count + 1

                            # Calculamos el tamaño de este gen vecino
                            current_length = int(especie['end'] - especie['start'])

                            # Algoritmo de máximos: Si este gen es más grande que el que teníamos guardado, lo actualizamos
                            if current_length > max_length:
                                max_length = current_length
                                # En el overlap de Ensembl el nombre viene en 'external_name'
                                max_name = especie['external_name']

                    # Cargamos la plantilla y cambiamos los "huecos" pasando a string
                    page = Path('html/geneOverlapStats.html').read_text()
                    contents = page.replace("{{gene}}", gene_name).replace("{{length}}", str(my_length)).replace(
                        "{{count}}", str(overlap_count)).replace("{{max_name}}", max_name).replace("{{max_length}}",
                                                                                                   str(max_length))

                else:
                    contents = "Error al conectar con el servicio de Overlap"
                    error_code = 500

            else:
                # Tu gestión de errores de siempre
                contents = Path('html/error.html').read_text().replace("{{message}}", "Original gene not found")
                error_code = 404

        #E
        elif resource == "/geneMutations":
            # Troceamos los dos parámetros a tu manera
            parts = params.split("&")
            gene_name = parts[0].split("=")[1]
            min_len = int(parts[1].split("=")[1])  # Convertimos a número para poder comparar

            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn2 = http.client.HTTPSConnection("rest.ensembl.org")

            # Petición 1: Conseguir el ID del gen
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name,
                         headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                my_id = data['id']

                # Petición 2: Conseguir los transcritos expandidos usando el ID
                conn2.request("GET", "/lookup/id/" + my_id + "?expand=1", headers={"Content-Type": "application/json"})
                response2 = conn2.getresponse()

                if response2.status == 200:
                    data2 = json.loads(response2.read().decode())
                    transcripts_list = data2['Transcript']  # Lista de Python con los transcritos

                    # Inicializamos variables a tu manera
                    list_html = ""
                    count = 0

                    for t in transcripts_list:
                        # Calculamos el tamaño del transcrito actual
                        t_length = int(t['end'] - t['start'])

                        # Filtrado por longitud mínima
                        if t_length >= min_len:
                            count = count + 1
                            list_html += "<li>Transcript ID: " + t['id'] + " (Length: " + str(t_length) + " bases)</li>"

                    if list_html == "":
                        list_html = "<li>No transcripts found longer than the minimum length</li>"

                    # Cargamos plantilla y cambiamos huecos
                    page = Path('html/geneMutations.html').read_text()
                    contents = page.replace("{{gene}}", gene_name).replace("{{count}}", str(count)).replace("{{list}}",
                                                                                                            list_html)
                else:
                    contents = "Error fetching transcripts"
                    error_code = 500
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Gene not found")
                error_code = 404



        #F
        elif resource == "/karyotypeBand":
            gene_name = params.split("=")[1]

            conn = http.client.HTTPSConnection("rest.ensembl.org")
            conn2 = http.client.HTTPSConnection("rest.ensembl.org")

            # Petición 1: Buscamos el gen original
            conn.request("GET", "/lookup/symbol/homo_sapiens/" + gene_name,
                         headers={"Content-Type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode())
                chromo = data['seq_region_name']
                banda_objetivo = data['karyotype_band']  # Guardamos el nombre de la banda (ej: "q21.1")

                # Petición 2: Pedimos todas las bandas de ese cromosoma
                conn2.request("GET", "/overlap/region/homo_sapiens/" + chromo + "?feature=band",
                              headers={"Content-Type": "application/json"})
                response2 = conn2.getresponse()

                if response2.status == 200:
                    data2 = json.loads(response2.read().decode())  # Es una lista con todas las bandas del cromosoma

                    # Inicializamos variables para buscar la banda exacta
                    band_size = 0

                    for b in data2:
                        # Buscamos la banda que se llame igual que la de nuestro gen
                        if b['id'] == banda_objetivo:
                            band_size = int(b['end'] - b['start'])
                            break  # Como ya la hemos encontrado, usamos tu truco del break para ahorrar tiempo

                    # Cargamos la plantilla
                    page = Path('html/karyotypeBand.html').read_text()
                    contents = page.replace("{{gene}}", gene_name).replace("{{band}}", banda_objetivo).replace(
                        "{{size}}", str(band_size))
                else:
                    contents = "Error fetching chromosome bands"
                    error_code = 500
            else:
                contents = Path('html/error.html').read_text().replace("{{message}}", "Gene not found")
                error_code = 404

        #error final
        else:
            contents = Path('html/error.html').read_text().replace("{{message}}", "Page not found")
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