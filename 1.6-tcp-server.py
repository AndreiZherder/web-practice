#!/usr/bin/python3

import socket

with socket.socket() as server:
    server.bind(('', 2222))
    server.listen(1)

    while True:
        conn, address = server.accept()
        with conn:
            print('Connected by {}'.format(address))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    if data == b'close':
                        conn.close()
                        print('Connection closed')
                        break
                    else:
                        print(data.decode())
                        conn.sendall(data)


