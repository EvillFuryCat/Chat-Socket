from calendar import c
import socket
from threading import Thread, active_count

HOST = "127.0.0.1"
PORT = 12345
clients = []

def new_client(connection: socket.socket, *args) -> None:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(f"{data}")
            connection.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server started")
    print("Waiting for client request..")
    s.listen()
    while True:
        conn, addr = s.accept()
        newthread = Thread(target=new_client, args=(conn, addr))
        newthread.start()
        print(f"[ACTIVE CONNECTIONS] {active_count() - 1 }")

