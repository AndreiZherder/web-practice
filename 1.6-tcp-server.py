#!/usr/bin/python3

import socket


def main():
    with socket.socket() as server:
        server.bind(('', 2222))
        server.listen(1)

        while True:
            conn, address = server.accept()
            with conn:
                print('{} connected'.format(address))
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print('Connection closed by {}'.format(address))
                        break
                    else:
                        if data == b'close':
                            print('Connection closed due to close command from {}'.format(address))
                            break
                        else:
                            print(data.decode())
                            conn.sendall(data)


if __name__ == '__main__':
    main()
