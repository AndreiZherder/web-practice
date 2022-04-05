import asyncio


@asyncio.coroutine
def serve_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print('Someone connected')
    while True:
        request = yield from reader.read(1024)
        if not request or request == b'close':
            writer.close()
            break
        response = handle_request(request)
        print(f'{request.decode()} {response.decode()}')
        writer.write(response)
        yield from writer.drain()


def handle_request(request: bytes) -> bytes:
    return request.decode().upper().encode()


@asyncio.coroutine
def main():
    server = yield from asyncio.start_server(serve_client, port=2222)
    try:
        yield from server.serve_forever()
    finally:
        server.close()
        yield from server.wait_closed()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
