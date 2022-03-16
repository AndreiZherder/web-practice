#!/usr/bin/python3

import socket
from select import select


class Server:
    def __init__(self, port: int):
        self.port = port
        self.inputs = set()

    def run_server(self):
        with socket.socket() as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('', self.port))
            server.listen()
            self.serve_forever(server)

    def serve_forever(self, server: socket.socket):
        self.inputs = {server}
        while True:
            inputs_ready, _, _ = select(self.inputs, [], [])
            for socket in inputs_ready:
                if socket == server:
                    self.accept_connection(server)
                else:
                    try:
                        self.serve_client(socket)
                    except ConnectionResetError:
                        socket.close()
                        self.inputs.discard(socket)

    def accept_connection(self, server: socket.socket):
        client, address = server.accept()
        print('Client #{} connected'.format(client.getpeername()))
        self.inputs.add(client)

    def serve_client(self, client: socket.socket):
        request = self.read_request(client)
        if not request:
            print('Client #{} disconnected'.format(client.getpeername()))
            raise ConnectionResetError
        if request == b'close':
            print('Client #{} sent close command. Connection closed'.format(client.getpeername()))
            raise ConnectionResetError
        response = self.handle_request(client, request)
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
