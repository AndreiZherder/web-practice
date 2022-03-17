#!/usr/bin/python3

import socket
from collections import deque
from select import select

class Server:
    def __init__(self, port: int):
        self.port = port
        self.inputs = {}
        self.outputs = {}
        self.tasks = deque()

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
                    reason, socket = next(task)
                    if reason == 'read':
                        self.inputs[socket] = task
                    if reason == 'write':
                        self.outputs[socket] = task
                except StopIteration:
                    pass
            inputs_ready, outputs_ready, _ = select(self.inputs, self.outputs, [])
            for socket in inputs_ready:
                self.tasks.append(self.inputs.pop(socket))
            for socket in outputs_ready:
                self.tasks.append(self.outputs.pop(socket))

    def accept_connection(self, server: socket.socket):
        while True:
            yield 'read', server
            client, address = server.accept()
            print('Client #{} connected'.format(client.getpeername()))
            self.tasks.append(self.serve_client(client))

    def serve_client(self, client: socket.socket):
        with client:
            while True:
                yield 'read', client
                request = self.read_request(client)
                if not request:
                    print('Client #{} disconnected'.format(client.getpeername()))
                    break
                if request == b'close':
                    print('Client #{} sent close command. Connection closed'.format(client.getpeername()))
                    break
                response = self.handle_request(client, request)
                yield 'write', client
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
