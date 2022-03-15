#!/usr/bin/python3

import socket
import threading


def run_server(port: int):
    with socket.socket() as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', port))
        server.listen()
        serve_forever(server)


def serve_forever(server: socket):
    cid = 0
    while True:
        client, address = server.accept()
        print('Client #{} ({}:{}) connected'.format(cid, address[0], address[1]))
        t = threading.Thread(target=serve_client, args=(client, cid))
        t.start()
        cid += 1


def serve_client(client: socket, cid: int):
    with client:
        while True:
            request = read_request(client)
            if not request:
                print('Client #{} disconnected'.format(cid))
                break
            if request == b'close':
                print('Client #{} sent close command. Connection closed'.format(cid))
                break
            response = handle_request(cid, request)
            write_response(client, response)


def read_request(client: socket) -> bytes:
    try:
        return client.recv(1024)
    except ConnectionResetError:
        return b''


def handle_request(cid: int, request: bytes) -> bytes:
    s = request.decode()
    print('Client #{} request: {}'.format(cid, s))
    return s.upper().encode()


def write_response(client: socket, response: bytes):
    client.sendall(response)


def main():
    run_server(2222)


if __name__ == '__main__':
    main()
