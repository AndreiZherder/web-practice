#!/usr/bin/python3

import socket
import selectors
from collections import deque


class Server:
    def __init__(self, port: int):
        self.port = port
        self.tasks = deque()
        self.selector = selectors.DefaultSelector()

    def run_server(self):
        with socket.socket() as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('', self.port))
            server.listen()
            self.serve_forever(server)

    def serve_forever(self, server: socket.socket):
        self.tasks.append(self.accept_connection(server))
        while True:
            while self.tasks:
                task = self.tasks.popleft()
                try:
                    events, socket = next(task)
                    self.selector.register(fileobj=socket, events=events, data=task)
                except StopIteration:
                    pass
            for k, events in self.selector.select():
                self.selector.unregister(k.fileobj)
                task = k.data
                self.tasks.append(task)

    def accept_connection(self, server: socket.socket):
        while True:
            yield selectors.EVENT_READ, server
            client, address = server.accept()
            print('Client #{} connected'.format(client.getpeername()))
            self.tasks.append(self.serve_client(client))

    def serve_client(self, client: socket.socket):
        with client:
            while True:
                yield selectors.EVENT_READ, client
                request = self.read_request(client)
                if not request:
                    print('Client #{} disconnected'.format(client.getpeername()))
                    break
                if request == b'close':
                    print('Client #{} sent close command. Connection closed'.format(client.getpeername()))
                    break
                response = self.handle_request(client, request)
                yield selectors.EVENT_WRITE, client
                self.write_response(client, response)

    def read_request(self, client: socket.socket) -> bytes:
        try:
            return client.recv(1024)
        except ConnectionResetError:
            return b''

    def handle_request(self, client: socket.socket, request: bytes) -> bytes:
        s = request.decode()
        print('Client #{} request: {}'.format(client.getpeername(), s))
        return s.upper().encode()

    def write_response(self, client: socket.socket, response: bytes):
        client.sendall(response)


def main():
    server = Server(2222)
    server.run_server()


if __name__ == '__main__':
    main()
