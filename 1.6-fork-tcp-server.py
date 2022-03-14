#!/usr/bin/python3

import os
import socket
import sys


def run_server(port: int):
    with socket.socket() as server:
        server.bind(('', port))
        server.listen(10)
        serve_forever(server)


def serve_forever(server: socket):
    cid = 0
    children = set()
    while True:
        client, address = server.accept()
        print('Client #{} ({}:{}) connected'.format(cid, address[0], address[1]))
        child_pid = serve_client(client, cid)
        children.add(child_pid)
        reap_children(children)
        cid += 1


def serve_client(client: socket, cid: int) -> int:
    with client:
        child_pid = os.fork()
        if child_pid == 0:  # child process
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
            sys.exit()
    return child_pid


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


def reap_children(children):
    for child_pid in children.copy():
        child_pid, status = os.waitpid(child_pid, os.WNOHANG)
        if child_pid:
            children.discard(child_pid)


def main():
    run_server(2222)


if __name__ == '__main__':
    main()
