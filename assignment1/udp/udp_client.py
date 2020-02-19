import socket
import time
import multiprocessing
import argparse

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "ping"

def send(id=0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(f"{id}:{MESSAGE}".encode(), (UDP_IP, UDP_PORT))
        data, ip = s.recvfrom(BUFFER_SIZE)
        print("received data: {}: {}".format(ip, data.decode()))
    except socket.error:
        print("Error! {}".format(socket.error))
        exit()

def get_client_id():
    id = input("Enter client id:")
    return id

def sendMessage(udpSocket, id, sequence, message):
    udpSocket.sendto(f"{id}:{sequence}:{message}".encode(), (UDP_IP, UDP_PORT))

def receiveMessage(udpSocket):
    data, ip = udpSocket.recvfrom(BUFFER_SIZE)
    return data, ip

def openFile():
    with open('upload.txt', 'r') as f:
        return f.readlines()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="client id")
    args = parser.parse_args()

    try:
        file = openFile()
        # id = get_client_id()
        id = args.id
        sequence = 0
        # sequence = SequenceCounter()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)

        while sequence < len(file):
            try:
                sendMessage(s, id, sequence, file[sequence].strip())
                data, ip = receiveMessage(s)
                split = data.decode().split(':')
                # if sequence == int(data.decode()):
                print("id received: {}".format(split[0]))
                if sequence == int(split[1]) and id == split[0]:
                    print("Received acknowledgement for sequence: {}".format(sequence))
                    sequence += 1
                else:
                    print("Did not receive acknowledgement for sequence: {}".format(sequence))
                    print("Resending packet...")
            except socket.timeout as e:
                print(e)

    except IOError as e:
        print(e)
    except socket.error:
        print("Error! {}".format(socket.error))
    except KeyboardInterrupt as e:
        print("Keyboard Interrupt detected...")

if __name__ == '__main__':
    main()