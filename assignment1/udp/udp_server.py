import socket
import asyncio

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "pong"
FILE_DATA = {}

# def listen_forever():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind(("", UDP_PORT))

#     while True:
#         # get the data sent to us
#         data, ip = s.recvfrom(BUFFER_SIZE)
#         print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))
#         # reply back to the client
#         s.sendto(MESSAGE.encode(), ip)

async def handleClient(udpSocket, ip, data):
    # print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))
    # split = data.decode().split(':')
    # udpSocket.sendto(':'.join(split[0:2]).encode(), ip)

    split = data.decode().split(':')
    if split[0] not in FILE_DATA:
        print("Accepting file upload from client: %s" % split[0])
        FILE_DATA[split[0]] = {"data" : [], "sequence" : -1}
    
    # if sequence is the next sequence, accept incoming file data
    if int(split[1]) == FILE_DATA["sequence"] + 1:
        FILE_DATA[split[0]]["data"].append(split[2])
        FILE_DATA[split[0]]["sequence"] = int(split[1])
    
    udpSocket.sendto(':'.join(split[0:2]).encode(), ip)

async def main():
    print("Press Ctrl + c to exit this server...")
    print("Server started at port %s" % UDP_PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))

    while True:
        data, ip = s.recvfrom(BUFFER_SIZE)
        await handleClient(s, ip, data)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(e)