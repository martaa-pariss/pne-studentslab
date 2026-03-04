from Seq1 import *
from Client0 import *

print("-----| Practice 2, Exercise 4 |------")
IP = "172.20.10.4"
PORT = 8080
c = Client(IP, PORT)

print("Sending a message to the server...")
s = Seq()
s.read_fasta("sequences/FRAT1.file")
string_seq = str(s)
for i in range(0,5):
    l = [9*i:10]
    print(l)

response = c.talk(str(s))
print(f"Response: {response}")
