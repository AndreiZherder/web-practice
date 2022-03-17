#!/usr/bin/python3
import selectors
import socket


class Server:
    def __init__(self, port: int):
        self.port = port
        self.selector = selectors.DefaultSelector()

    def run_server(self):
        with socket.socket() as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('', self.port))
            server.listen()
            self.selector.register(fileobj=server, events=selectors.EVENT_READ, data=self.accept_connection)
            self.serve_forever()

    def serve_forever(self):
        while True:
            for k, _ in self.selector.select():
                callback = k.data
                callback(k.fileobj)

    def accept_connection(self, server: socket.socket):
        client, address = server.accept()
        print('Client #{} connected'.format(client.getpeername()))
        self.selector.register(fileobj=client, events=selectors.EVENT_READ, data=self.serve_client)

    def serve_client(self, client: socket.socket):
        try:
            request = self.read_request(client)
            if not request:
                print('Client #{} disconnected'.format(client.getpeername()))
                raise ConnectionResetError
            if request == b'close':
                print('Client #{} sent close command. Connection closed'.format(client.getpeername()))
                raise ConnectionResetError
        except ConnectionResetError:
            self.selector.unregister(client)
            client.close()
            return
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
