import socket

# estamos configurando el servidor, esto se copia y se pega, solo cambiamos el ip para q funcione en el ordenador
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
PORT = 8080
IP = "212.128.255.91"
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()
print("The server is configured!")

#Aquí empieza la programacion que tenemos que hacer
seq_list = ["ACGT", "CATG", "GATC", "TAGC", "AAAA"]
while True:
    print("Waiting for Clients to connect")
    (cs, client_ip_port) = ls.accept()
    print("A client has connected to the server!")
    msg_raw = cs.recv(2048)
    msg = msg_raw.decode()
    l = msg.strip().split(" ")  # esto lo hemos implementado para la segunda tarea, para separar los get de los numeros ¡OJO CON EL PING; SOLO TIENE UNA PALABRA!
    cmd = l[0]
    param = l[1]
    if len(l) < 1:
        if msg.strip() == "PING":
            print(" PING command... \n OK!")
            response = f"OK! \n "
            cs.send(response.encode())
    elif len(l) == 2:
        if cmd == "GET":
            if param == "0":
                s = seq_list[0] #s stands for chosen sequence
                print(f" GET \n {s}")
                response = f"´{s} \n "
                cs.send(response.encode())
            elif param == "1":
                s = seq_list[1]
                print(f" GET \n {s}")
                response = f"´{s} \n "
                cs.send(response.encode())
            elif param == "2":
                s = seq_list[2]
                print(f" GET \n {s}")
                cs.send(response.encode())
            elif pa
                response = f"´{s} \n "ram == "3":
                s = seq_list[3]
                print(f" GET \n {s}")
                response = f"´{s} \n "
                cs.send(response.encode())
            elif param == "4":
                s = seq_list[4]
                print(f" GET \n {s}")
                response = f"´{s} \n "
                cs.send(response.encode())



    cs.close()
