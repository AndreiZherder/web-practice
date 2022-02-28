import socket


def main():
    with socket.socket() as conn:
        address = ('185.187.91.100', 2222)
        conn.connect(address)
        print('Connected to {}:{}'.format(address[0], address[1]))
        while True:
            data = input('Enter data: ').encode()
            conn.sendall(data)
            data = conn.recv(1024)
            if not data:
                print('Connection closed by server')
                break
            print(data.decode())


if __name__ == '__main__':
    main()
