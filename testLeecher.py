from socket import *

def leecher():
    serverName = "192.168.1.111" #my current IP address, change to the IP address of person running the code
    serverPort = 12000 #random port number
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    sentence = input("Input the file you want to download: ")
    #file = open(sentence, "r") 
    clientSocket.send(sentence.encode())
    recvdFile = clientSocket.recv(1024).decode()
    _, filename = recvdFile.split()
    with open(filename, "wb") as file:
        while chunk:= clientSocket.recv(1024):
            file.write(chunk)

    choice = input("File has been Downloaded, would you like to become a seeder?")
    #print("From Server: ", modifiedSentence.decode())
    clientSocket.close()

if __name__ == "__main__":
    leecher()