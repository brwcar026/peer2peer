from socket import *

seeders = {}

def tracker():
    udp_trackerPort = 12002
    udp_IP = "192.168.1.111"
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind((udp_IP, udp_trackerPort))
    print("The server is ready to track available seeders")
    while True:
        message, clientAddress = udpSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        udpSocket.sendto(modifiedMessage.encode(), clientAddress)

if __name__ == "__main__":
    tracker()