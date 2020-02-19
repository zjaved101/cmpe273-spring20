import socket
import asyncio

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "pong"

def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))

    while True:
        # get the data sent to us
        data, ip = s.recvfrom(BUFFER_SIZE)
        print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))
        # reply back to the client
        s.sendto(MESSAGE.encode(), ip)

async def handleClient(udpSocket, ip, data):
    print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))
    split = data.decode().split(':')
    # print("SEQUENCE: {}".format(split[1]))
    # udpSocket.sendto(split[1].encode(), ip)
    # split = ['1','0',split[-1]]
    udpSocket.sendto(':'.join(split[0:2]).encode(), ip)

async def main():
    print("Press Ctrl + c to exit this server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))

    while True:
        # print('Waiting for clients...')
        data, ip = s.recvfrom(BUFFER_SIZE)
        # print('Handling client: {}'.format(ip))
        await handleClient(s, ip, data)
        # print('Handled client: {}'.format(ip))

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(e)