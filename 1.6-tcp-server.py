#!/usr/bin/python3

import socket


def main():
    with socket.socket() as server:
        server.bind(('', 2222))
        server.listen(1)

        while True:
            try:
                conn, address = server.accept()
            except KeyboardInterrupt:
                print('Closed by user')
                return
            with conn:
                print('Connected by {}'.format(address))
                while True:
                    try:
                        data = conn.recv(1024)
                    except KeyboardInterrupt:
                        print('Closed by user')
                        return
                    if not data:
                        print('Connection closed by client {}'.format(address))
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
