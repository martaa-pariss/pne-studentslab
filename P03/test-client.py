from imports import Client
IP = "212.128.255.91"
PORT = 8080
print("-----| Practice 3, Exercise 7 |------")

# Create the client
c = Client(IP, PORT)

# Print info
print(c)
print("* Testing PING...")
response = c.talk("PING")
print(response)

print("* Testing GET...")

seq0 = c.talk("GET 0").strip()
print("GET 0:", seq0)

seq1 = c.talk("GET 1").strip()
print("GET 1:", seq1)

seq2 = c.talk("GET 2").strip()
print("GET 2:", seq2)

seq3 = c.talk("GET 3").strip()
print("GET 3:", seq3)

seq4 = c.talk("GET 4").strip()
print("GET 4:", seq4)

print("\n* Testing INFO...")
response = c.talk("INFO " + seq0)
print(response)

print("* Testing COMP...")
print("COMP", seq0)
response = c.talk("COMP " + seq0)
print(response)

print("* Testing REV...")
print("REV", seq0)
response = c.talk("REV " + seq0)
print(response)

print("* Testing GENE...")

genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

for gene in genes:
    print("GENE", gene)
    response = c.talk("GENE " + gene)
    print(response)