import socket
import asyncio

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print(f'Connection address:{addr}')

    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: 
            print('No data received.')
            break
        print(f"received data:{data.decode()}")
        conn.send("pong".encode())

    conn.close()

def listen():
    '''
        Listens for connections coming from clients
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print(f'Connection address:{addr}')

    return conn, addr

async def handleClient(reader, writer):
    data = await reader.read(BUFFER_SIZE)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print('Connection address:%s Message: %s' % (addr, message))

    writer.write("pong".encode())
    await writer.drain()

    writer.close()

async def main():
    print("Press Ctrl + c to exit this server...")
    server = await asyncio.start_server(handleClient, TCP_IP, TCP_PORT)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(e)