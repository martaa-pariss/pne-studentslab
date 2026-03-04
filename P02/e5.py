from Seq1 import *
from Client0 import *

print("-----| Practice 2, Exercise 5 |------")
IP = "172.20.10.4"
PORT = 8080
c = Client(IP, PORT)

print("Sending a message to the server...")
s = Seq()
s.read_fasta("sequences/FRAT1.file")
string_seq = str(s)
first_50_bases = string_seq[:50]
print("Gene FRAT1:", first_50_bases)
for i in range(0,5):
    l = first_50_bases[i*10:(i+1)*10]
    print(f"Fragment{i+1}: {l}")

response = c.talk(l)
print(f"Response: {response}")
