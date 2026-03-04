import socket
class Client:
    def __init__(self, ip, port):
        #constructor
        self.ip = ip
        self.port = port

    def __str__(self):
        #especifica las conexiones (dice el nombre del servidor y del puerto)
        response = f"Connection to SERVER at {self.ip}, PORT: {self.port}" #muy importante poner lo del self, sino no va
        return response

    def ping(self):
        print("OK")

    def talk(self, msg):
        # -- Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # establish the connection to the Server (IP, PORT)
        s.connect((self.ip, self.port))
        # Send data.
        s.send(str.encode(msg))
        # Receive data
        response = s.recv(2048).decode("utf-8")
        # Close the socket
        s.close()
        # Return the response
        return response

