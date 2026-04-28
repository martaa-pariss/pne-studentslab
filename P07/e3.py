import http.client
import json

SERVER = "rest.ensembl.org"
ENDPOINT = "/sequence/id"
PARAMS = "/ENSG00000207552?content-type=application/json"
URL = "https://" + SERVER + ENDPOINT + PARAMS
print()
print(f"server: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPConnection(SERVER)
try:
    headers = {"Content-Type": "application/json"}
    conn.request("GET", ENDPOINT + PARAMS, headers=headers)
    response = conn.getresponse()
    print(f"Response received!: {response.status} {response.reason}")
    print()
    if response.status == 200:
        data = response.read().decode("utf-8")
        decoded = json.loads(data)
        print(f"Gene: MIR633")
        print(f"Description: {decoded['desc']}")
        print(f"Bases: {decoded['seq']}")
    else:
        print(f"Error en la consulta: {response.status}")


except Exception as e:
    print(f"ERROR ON: {e}")

