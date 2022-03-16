#!/usr/bin/python3

import socket
from select import select


class Server:
    def __init__(self, port: int):
        self.port = port
        self.inputs = set()
        self.outputs = dict()

    def run_server(self):
        with socket.socket() as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('', self.port))
            server.listen()
            self.serve_forever(server)

    def serve_forever(self, server: socket):
        self.inputs = {server}
        self.outputs = dict()
        while True:
            inputs_ready, outputs_ready, _ = select(self.inputs, self.outputs, [])
            for socket in inputs_ready:
                if socket == server:
                    client, address = server.accept()
                    print('Client #{} connected'.format(client.getpeername()))
                    self.inputs.add(client)
                else:
                    try:
                        self.serve_client(socket)
                    except ConnectionResetError:
                        socket.close()
                        self.inputs.discard(socket)
            for client in outputs_ready:
                if client in self.outputs:
                    self.write_response(client)
                    del self.outputs[client]

    def serve_client(self, client: socket):
        request = self.read_request(client)
        if not request:
            print('Client #{} disconnected'.format(client.getpeername()))
            raise ConnectionResetError
        if request == b'close':
            print('Client #{} sent close command. Connection closed'.format(client.getpeername()))
            raise ConnectionResetError
        response = self.handle_request(client, request)
        self.prepare_response(client, response)

    def read_request(self, client: socket) -> bytes:
        try:
            return client.recv(1024)
        except ConnectionResetError:
            return b''

    def handle_request(self, client: socket, request: bytes) -> bytes:
        s = request.decode()
        print('Client #{} request: {}'.format(client.getpeername(), s))
        return s.upper().encode()

    def prepare_response(self, client: socket, response: bytes):
        self.outputs[client] = response

    def write_response(self, client: socket):
        client.sendall(self.outputs[client])


def main():
    server = Server(2222)
    server.run_server()


if __name__ == '__main__':
    main()
