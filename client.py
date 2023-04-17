import socket, threading

HOST = "127.0.0.1"
PORT = 12345


def new_connect(conn: socket.socket) -> None:
    
    def get_message() -> None:
        while True:
            data = conn.recv(1024)
            if not data:
                print("Connection closed by the server")
                break
            print(data.decode())
    
    def send_message() -> None:
        user_name = input('What is your name?\n')
        user_name = '@' + user_name.encode("UTF-8").decode("UTF-8")
        output_message = user_name.encode()
        conn.sendall(output_message)
        print('To exit from chat write ":q" and press "enter"')
        while True:
            user_message = input()
            user_message = user_message.encode("UTF-8").decode("UTF-8")

            if user_message == ':q':
                conn.sendall(user_message.encode())
                break

            output_message = f'{user_name}: {user_message}'.encode()
            conn.sendall(output_message)

    get = threading.Thread(target=get_message)
    get.start()
    send = threading.Thread(target=send_message)
    send.start()

    get.join()
    send.join()
    conn.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        new_connect(s)