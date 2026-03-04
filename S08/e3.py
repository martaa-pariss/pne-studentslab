import socket

# SERVER IP, PORT
PORT = 8081
IP = "212.128.255.64" # it depends on the machine the server is running

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((IP, PORT))

s.send(str.encode("HOLAA!!!"))

# Close the socket
s.close()

