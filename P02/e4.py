from Seq1 import *
from Client0 import *

print("-----| Practice 2, Exercise 4 |------")
IP = "172.20.10.4"
PORT = 8080
c = Client(IP, PORT)

print("Sending a message to the server...")
genes = ["ADA", "FRAT1", "U5"]
FOLDER = "sequences/"
for gene in genes:

    print(f"\nGene: {gene}")

    filename = FOLDER + gene + ".file"

    s = Seq()
    s.read_fasta(filename)
    response = c.talk(str(s))
    print(f"Response: {response}")


