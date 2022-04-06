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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(serve_client, port=2222))
    loop.run_forever()
