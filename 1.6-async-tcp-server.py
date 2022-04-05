import asyncio


async def serve_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print('Someone connected')
    while True:
        request = await reader.read(1024)
        if not request or request == b'close':
            writer.close()
            break
        response = handle_request(request)
        print(f'{request.decode()} {response.decode()}')
        writer.write(response)
        await writer.drain()


def handle_request(request: bytes) -> bytes:
    return request.decode().upper().encode()


async def main():
    server = await asyncio.start_server(serve_client, port=2222)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
