import socket
#we need to create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#establish the connection to the server (IP, PORT)
s.connect((IP, PORT))
#Send data. No string can be sent, only bites
#it is necessary to encode the string into bytes
s.send(str.encode("Holaaa!!!"))
#close the socket when the comunicatios is done: open file, use file, close file
s.close()

#si queremos recibir el mensaje
msg = s.recv(1024) #el numero de dentro es el numero máximo de caracteres que puede tener el mensaje que queremos recibir
print(msg.decode())