import socket


def main():
    with socket.socket() as conn:
        address = ('127.0.0.1', 2222)
        conn.connect(address)
        print('Connected to {}:{}'.format(address[0], address[1]))
        while True:
            data = input('Enter data: ').encode()
            if data:
                conn.sendall(data)
                data = conn.recv(1024)
                if not data:
                    print('Connection closed by server')
                    break
                print(data.decode())


if __name__ == '__main__':
    main()
