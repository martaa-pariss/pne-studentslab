import http.client
import json

SERVER = "rest.ensembl.org"
ENDPOINT = "/info/ping"
PARAMS = "?content-type=application/json"
URL = SERVER + ENDPOINT + PARAMS

print()
print(f"server: {SERVER}")
print(f"URL: {URL}")

try:
    conn = http.client.HTTPConnection(SERVER)
    print("PING OK! The database is running")
except Exception as e:
    print("not connected:", e)