import http.client
import json

#sigue sin irme el import
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
ENDPOINT = "/sequence/id/"

genes = {
    "FRAT1": "ENSG00000165879",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6_269P": "ENSG00000206621",
    "MIR633": "ENSG00000207552",
    "TTTY4C": "ENSG00000228658",
    "RBMY2YP": "ENSG00000226374",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

PARAMS2 = "?content-type=application/json"

conn = http.client.HTTPConnection(SERVER)

for gene_name, gene_id in genes.items():

    #print("\n-----------------------------")
    print(f"Gene: {gene_name}")

    try:
        headers = {"Content-Type": "application/json"}
        conn.request("GET", ENDPOINT + gene_id + PARAMS2, headers=headers)
        response = conn.getresponse()

        if response.status == 200:
            data = response.read().decode("utf-8")
            decoded = json.loads(data)

            print(f"Description: {decoded.get('desc', 'No description')}")
            print(f"Length: {len(decoded['seq'])}")

            seq_obj = Seq(decoded['seq'])

            BaseCount = seq_obj.count()
            print(f"Bases Count: {BaseCount}")

            PercentOfEachBase = seq_obj.percentage()
            print(f"Percent of Bases: {PercentOfEachBase}")

            MostBase = seq_obj.max_base()
            print(f"Most frequent base: {MostBase}")
            print("--------------------------------------------------\n")

        else:
            print(f"Error en la consulta: {response.status}")

    except Exception as e:
        print(f"ERROR ON: {e}")