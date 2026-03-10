import socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
PORT = 8080
IP = "172.20.10.4"
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()
print("The server is configured!")
connection_count = 0
while True:
    print("Waiting for Clients to connect")
    (cs, client_ip_port) = ls.accept()
    connection_count += 1
    print("A client has connected to the server!")
    msg_raw = cs.recv(2048)
    msg = msg_raw.decode()
    print(f"CONNECTION {connection_count} Client IP, PORT: {client_ip_port}")
    print(f"Message received: {msg}")
    response = f"ECHO:{msg}\n"
    cs.send(response.encode())
    cs.close()