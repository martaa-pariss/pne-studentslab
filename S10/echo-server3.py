import socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
PORT = 8080
IP = "212.128.255.92"
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()
print("The server is configured!")
connection_count = 0
client_list = []
while True:
    print("Waiting for Clients to connect")
    (cs, client_ip_port) = ls.accept()
    connection_count += 1
    client_list.append(client_ip_port)
    print("A client has connected to the server!")
    msg_raw = cs.recv(2048)
    msg = msg_raw.decode()
    print(f"CONNECTION {connection_count} Client IP, PORT: {client_ip_port}")
    print(f"Message received: {msg}")
    response = f"ECHO:{msg}\n"
    cs.send(response.encode())
    cs.close()

    #voy a poner un limite de 5 porque si lo tengo q parar yo me da error y me sale todo rojo
    if connection_count == 5:
        print("The total clients connected is:\n")
        for client in client_list:
            print(client)

        print("Finished")
        break
ls.close()