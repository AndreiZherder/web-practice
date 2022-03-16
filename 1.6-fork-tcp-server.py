#!/usr/bin/python3

import os
import socket
import sys


def run_server(port: int):
    with socket.socket() as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', port))
        server.listen(10)
        serve_forever(server)


def serve_forever(server: socket.socket):
    children = set()
    while True:
        client, address = server.accept()
        print('Client #{} connected'.format(client.getpeername()))
        child_pid = serve_client(client)
        children.add(child_pid)
        reap_children(children)


def serve_client(client: socket.socket) -> int:
    with client:
        child_pid = os.fork()
        if child_pid == 0:  # child process
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
            sys.exit()
    return child_pid


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


def reap_children(children):
    for child_pid in children.copy():
        child_pid, status = os.waitpid(child_pid, os.WNOHANG)
        if child_pid:
            children.discard(child_pid)


def main():
    run_server(2222)


if __name__ == '__main__':
    main()
