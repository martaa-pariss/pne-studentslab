from Seq1 import *
from Client0 import *

print("-----| Practice 2, Exercise 6 |------")

# 🔹 Servidor 1
IP1 = "172.20.10.4"
PORT1 = 8080
c1 = Client(IP1, PORT1)

# 🔹 Servidor 2
IP2 = "172.20.10.4"
PORT2 = 8080
c2 = Client(IP2, PORT2)

print(c1)
print(c2)

# Leer secuencia
s = Seq()
s.read_fasta("sequences/FRAT1.file")

string_seq = str(s)
first_50 = string_seq[:50]
print("Gene FRAT1:", first_50)

for i in range(5):
    l = first_50[i * 10:(i + 1) * 10]
    print(f"Fragment {i + 1}: {l}")

    response1 = c1.talk(l)
    print(f"Server 1 response: {response1}")

    response2 = c2.talk(l)
    print(f"Server 2 response: {response2}")