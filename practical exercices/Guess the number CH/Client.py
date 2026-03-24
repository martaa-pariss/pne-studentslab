import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 5050))

    print("Guess the number CH (1-100)")

    while True:
        try:
            guess = input("Enter your guess: ")

            client.send(guess.encode())

            response = client.recv(1024).decode()

            if response == "Higher":
                print("Higher!")
            elif response == "Lower":
                print("Lower!")
            else:
                print(f"{response}")
                break

        except:
            print("Error in connection")
            break

    client.close()


if __name__ == "__main__":
    start_client()