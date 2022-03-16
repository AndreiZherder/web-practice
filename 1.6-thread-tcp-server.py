#!/usr/bin/python3

import socket
import threading


def run_server(port: int):
    with socket.socket() as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', port))
        server.listen()
        serve_forever(server)


def serve_forever(server: socket.socket):
    while True:
        client, address = server.accept()
        print('Client #{} connected'.format(client.getpeername()))
        t = threading.Thread(target=serve_client, args=(client,))
        t.start()


def serve_client(client: socket.socket):
    with client:
        while True:
            request = read_request(client)
            if not request:
                print('Client #{} disconnected'.format(client.getpeername()))
                break
            if request == b'close':
                print('Client #{} sent close command. Connection closed'.format(client.getpeername()))
                break
            response = handle_request(client, request)
            write_response(client, response)


def read_request(client: socket.socket) -> bytes:
    try:
        return client.recv(1024)
    except ConnectionResetError:
        return b''


def handle_request(client: socket.socket, request: bytes) -> bytes:
    s = request.decode()
    print('Client #{} request: {}'.format(client.getpeername(), s))
    return s.upper().encode()


def write_response(client: socket.socket, response: bytes):
    client.sendall(response)


def main():
    run_server(2222)


if __name__ == '__main__':
    main()
