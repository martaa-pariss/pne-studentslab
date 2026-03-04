from Client0 import Client

print("-----| Practice 2, Exercise 3 |------")

# -- Parameters of the server to talk to
IP = "172.20.10.4" # your IP address
PORT = 8080
# -- Create a client object
c = Client(IP, PORT)

print("Sending a message to the server...")
response = c.talk("Testing!!!")
print(f"Response: {response}")


#no me funcionaba porque no etnia ningun servidor correindo, HAY QUE TENER UN SERVIDOR CORRIENDO, CON EL MISMO PORT, ya que es con quien estas hablando