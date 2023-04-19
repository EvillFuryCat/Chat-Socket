import socket
import json
import threading
import datetime

class ChatServer:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.clients = []
        self.names = {}
        self.lock = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.cur_data = datetime.datetime.now().strftime("%d.%m.%Y")
        self.history = {
            "clients": {},
            "log": []
        }

    def listen_for_clients(self) -> None:
        self.socket.listen()
        print(f"[SERVER RUNNUNG ON {self.host}:{self.port}]")
        while True:
            conn, addr = self.socket.accept()
            print(f"New client connected: {addr}")
            thread = threading.Thread(target=self.handle_client, args=(conn,))
            thread.start()

    def handle_client(self, conn) -> None:
        with self.lock:
            self.clients.append(conn)
        name = conn.recv(1024).decode()
        with self.lock:
            self.names[conn] = name
        message = f"{name} has joined the chat"
        print(message)
        self.broadcast(message.encode(), conn)
        while True:
            try:
                data = conn.recv(1024)
            except:
                with self.lock:
                    self.clients.remove(conn)
                    name = self.names[conn]
                    del self.names[conn]
                message = f"{name} has left the chat"
                print(message)
                self.broadcast(message.encode())
                break
            if not data:
                with self.lock:
                    self.clients.remove(conn)
                    name = self.names[conn]
                    del self.names[conn]
                message = f"{name} has left the chat"
                print(message)
                self.broadcast(message.encode())
                break
            cur_time = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M")
            message = f"{cur_time} {self.names[conn]}|> {data.decode()}"
            self.history["log"].append(message)
            self.history["clients"][name] = str(conn)
            self.save_history(self.history)
            print(message)
            self.broadcast(message.encode(), conn)

    def broadcast(self, message, sender=None):
        with self.lock:
            for conn in self.clients:
                if conn != sender:
                    conn.sendall(message)

    def save_history(self, data):
        with open(f'server_log{self.cur_data}.json', "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    server = ChatServer("127.0.0.1", 12345)
    server.listen_for_clients()

