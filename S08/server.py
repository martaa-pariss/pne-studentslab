#172.20.10.4
import socket

HOST = "172.20.10.4"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()

print("Servidor esperando conexion...")


conn, addr = server.accept()
print("Conectando con: ", addr)


while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Mensaje recibido: ", data.decode())
    conn.sendall(data)

conn.close()
server.close()
