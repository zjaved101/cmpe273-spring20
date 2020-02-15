import socket
import asyncio


TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "ping"

def send(id=0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(f"{id}:{MESSAGE}".encode())
    data = s.recv(BUFFER_SIZE)
    s.close()
    print("received data:", data.decode())


def get_client_id():
    id = input("Enter client id:")
    return id

async def main():
    print("Press Ctrl + c to quit client")
    id = get_client_id()
    try:
        while True:
            reader, writer = await asyncio.open_connection(TCP_IP, TCP_PORT)
            message = "%s:ping" % (id)
            writer.write(message.encode())
            data = await reader.read(BUFFER_SIZE)
            print("Received data:%s" % data.decode())
            writer.close()
    except KeyboardInterrupt:
        print("Client closed...")

    writer.close()

if __name__ == "__main__":
    asyncio.run(main())