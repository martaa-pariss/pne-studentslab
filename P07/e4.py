from Seq1 import *
#NAME, DESCRIPTION (LIKE E3), LEN, NUMBER Of TOTAL BASES, PERCENTAGE OF EACH BASE, MOST FREQ BASE
import http.client
import json

####defino las funciones qui porque no me va el import
class Seq:
    def __init__(self, strbases):
        self.strbases = strbases
        self.invalid = False  # puedes mejorar esta validación si quieres

    def count(self):
        bases_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        if self.strbases is None or self.invalid:
            return bases_dict
        for base in self.strbases:
            bases_dict[base] += 1
        return bases_dict

    def percentage(self):
        bases_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

        if self.strbases is None or self.invalid:
            return bases_dict

        total = len(self.strbases)
        counts = self.count()

        for base in bases_dict:
            bases_dict[base] = (counts[base] / total) * 100

        return bases_dict

    def max_base(self):
        percentages = self.percentage()

        if self.strbases is None or self.invalid:
            return None

        max_base = max(percentages, key=percentages.get)
        return max_base, percentages[max_base]
####este ya es el programa que toca

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
        print(f"Length: {len(decoded['seq'])}")
        #a partir de aqui necesito usar la clase asi q lo hago diferente
        seq_obj = Seq(decoded['seq'])
        BaseCount = seq_obj.count()
        print(f"Bases Count: {BaseCount}")
        PercentOfEachBase = seq_obj.percentage()
        print(f"Percent of Bases: {PercentOfEachBase}")
        MostBase = seq_obj.max_base()
        print(MostBase)
    else:
        print(f"Error en la consulta: {response.status}")


except Exception as e:
    print(f"ERROR ON: {e}")

