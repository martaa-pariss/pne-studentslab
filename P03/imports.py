class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases=None):
        valid_bases = ['A', 'C', 'G', 'T']

        self.strbases = None
        self.invalid = False

        if strbases is None:
            print("NULL sequence created")
        else:
            for base in strbases:
                if base not in valid_bases:
                    print("INVALID sequence!")
                    self.invalid = True
                    return

            self.strbases = strbases
            print("New sequence created!")

    def __str__(self):
        if self.invalid:
            return "ERROR"
        if self.strbases is None:
            return "NULL"
        return self.strbases

    def __len__(self):
        if self.strbases is None or self.invalid:
            return 0
        return len(self.strbases)

    def len(self):
        return len(self.strbases)

    def count_base(self, base):
        if self.strbases is None or self.invalid:
            return 0
        return self.strbases.count(base)

    def count(self):
        bases_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        if self.strbases is None or self.invalid:
            return bases_dict
        for base in self.strbases:
            bases_dict[base] += 1
        return bases_dict

    def reverse(self):
        if self.strbases is None or self.invalid:
            return str(self)
        return self.strbases[::-1]

    def complement(self):
        if self.strbases is None or self.invalid:
            return str(self)
        comp_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join([comp_dict[base] for base in self.strbases])

    def read_fasta(self, filename):
        sequence = ""
        with open(filename, "r") as f:
            for line in f:
                if line.startswith(">"):
                    continue
                sequence += line.strip()

        self.strbases = sequence


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