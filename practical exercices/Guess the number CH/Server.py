import socket
import random
import threading

class NumberGuesser:
    def __init__(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = []

    def guess(self, number):
        self.attempts.append(number)

        if number == self.secret_number:
            return f"You won after {len(self.attempts)} attempts"
        elif number > self.secret_number:
            return "Lower"
        else:
            return "Higher"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    game = NumberGuesser()

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            number = int(data)
            response = game.guess(number)

            conn.send(response.encode())

            if "won" in response:
                break

        except:
            break

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5050))
    server.listen()

    print("[SERVER STARTED] Waiting for connections...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()