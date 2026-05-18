import http.client
import json


def hacer_peticion_json(endpoint):
    print(f"\n==========================================")
    print(f"Requesting JSON data: {endpoint}")
    print(f"==========================================")
    try:
        # Se conecta localmente a tu servidor en el puerto 8080
        conn = http.client.HTTPConnection("localhost", 8080)
        conn.request("GET", endpoint)
        response = conn.getresponse()

        print(f"Status code HTTP: {response.status}")
        raw_body = response.read().decode()

        if response.status == 200:
            # Procesamos el JSON e imprimimos la información limpia en la consola
            objeto_json = json.loads(raw_body)
            print("Información formateada e impresa por consola:")
            print(json.dumps(objeto_json, indent=4, ensure_ascii=False))
        else:
            print(f"Error returned from the server: {raw_body}")

    except Exception as e:
        print(f"Error connecting the server: {e}")


if __name__ == "__main__":
    print("Welcome to JSON client!!!")
#test everything in the server
    hacer_peticion_json("/listSpecies?limit=3&json=1")
    hacer_peticion_json("/karyotype?species=human&json=1")
    hacer_peticion_json("/chromosomeLength?species=human&chromo=7&json=1")
    hacer_peticion_json("/geneLookup?gene=FRAT1&json=1")
    hacer_peticion_json("/geneSeq?gene=FRAT1&json=1")
    hacer_peticion_json("/geneInfo?gene=FRAT1&json=1")
    hacer_peticion_json("/geneCalc?gene=FRAT1&json=1")
    hacer_peticion_json("/geneList?chromo=9&start=22125500&end=22136000&json=1")