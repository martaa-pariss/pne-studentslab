import http.client
import json

SERVER = "rest.ensembl.org"
ENDPOINT = "/info/ping"
PARAMS = "?content-type=application/json"
URL = SERVER + ENDPOINT + PARAMS

print()
print(f"server: {SERVER}")
print(f"URL: {URL}")

#aqui falta lo del ping ok! the database is running

#connect with the server
conn = http.client.HTTPConnection(SERVER)