import socket
import termcolor
# -- Server network parameters
IP = "212.128.255.99"
PORT = 8080
def process_client(s):
    # -- Receive the request message
    req_raw = s.recv(2000)
    req = req_raw.decode()

    print("Message FROM CLIENT: ")
    termcolor.cprint(req, "green")


# -------------- MAIN PROGRAM
# ------ Configure the server
# -- Listening socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Setup up the socket's IP and PORT
ls.bind((IP, PORT))

# -- Become a listening socket
ls.listen()

print("Echo server configured!")

# --- MAIN LOOP
while True:
    print("Waiting for clients....")
    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server stopped!")
        ls.close()
        exit()
    else:

        # Service the client
        process_client(cs)

        # -- Close the socket
        cs.close()


#he puesto en la terminal "echo "Hello!" | nc 212.128.255.99 8080" mientres este codigo estaba en marcha y en pycharm se me ha impreso "Hello!" sin las comillas
#en la segunda tarea, le hemos dado al play a este codigo y hemos escrito en firefox (en la barra) : http://212.128.255.99:8080/hello
    #Esto es lo que ha impreso la máquina:
    #Message FROM CLIENT:
        #GET /hello HTTP/1.1
        #Host: 212.128.255.99:8080
        #User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0
        #Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
        #Accept-Language: ca-valencia,ca;q=0.9,en-US;q=0.8,en;q=0.7
        #Accept-Encoding: gzip, deflate
        #Connection: keep-alive
        #Upgrade-Insecure-Requests: 1
        #Priority: u=0, i