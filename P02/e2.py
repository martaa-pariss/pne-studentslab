from Client0 import Client

print("-----| Practice 2, Exercise 2 |------")
# -- Parameters of the server to talk to
IP = "172.20.10.4" # your IP address
PORT = 8080
# -- Create a client object
c = Client(IP, PORT)
# -- Test the ping method
c.__str__()