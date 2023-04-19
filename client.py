import socket
import threading

class ChatClient:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.name = input("Enter your name: ")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.sendall(self.name.encode())
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        
    def receive_messages(self):
        while True:
            data = self.socket.recv(1024)
            if not data:
                print("Connection closed")
                self.socket.close()
                break
            print(data.decode())

    def send_message(self, message):
        self.socket.sendall(message.encode())

if __name__ == "__main__":
    client = ChatClient("127.0.0.1", 12345)
    while True:
        message = input()
        client.send_message(message)