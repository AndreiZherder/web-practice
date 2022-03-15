#!/usr/bin/python3

import socket


def main():
    with socket.socket() as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', 2222))
        server.listen(1)

        while True:
            conn, address = server.accept()
            with conn:
                print('{}:{} connected'.format(address[0], address[1]))
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print('Connection closed by {}:{}'.format(address[0], address[1]))
                        break
                    else:
                        if data == b'close':
                            print('Received close command from {}:{}. Connection closed'.format(address[0], address[1]))
                            break
                        else:
                            print(data.decode())
                            conn.sendall(data)


if __name__ == '__main__':
    main()
