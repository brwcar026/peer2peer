from socket import *

def seeder():
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("0.0.0.0",serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive")
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        filename = connectionSocket.recv(1024).decode()
        #capitalizedSentence = sentence.upper()
        print("file to be sent: ", filename)
        with open(filename, "rb") as file:
            content = file.read(1024)
            connectionSocket.send(content)
        #file = open(filename, "rb")
        #connectionSocket.send(capitalizedSentence.encode())
        connectionSocket.close()

if __name__ == "__main__":
    seeder()