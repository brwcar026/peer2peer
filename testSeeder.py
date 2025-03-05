from socket import *

def seeder():
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("0.0.0.0",serverPort))
    serverSocket.listen(1)
    print("The server is ready to send a file")
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Connected to Leecher at: ", addr)
        filename = connectionSocket.recv(1024).decode()
        #capitalizedSentence = sentence.upper()
        print("File to be sent: ", filename)
        with open(filename, "rb") as file:
            content = file.read(1024)
            connectionSocket.send(content)

            while chunk:= file.read(1024):
                connectionSocket.send(chunk)

        print("File sent successfully!")
        #file = open(filename, "rb")
        #connectionSocket.send(capitalizedSentence.encode())
        connectionSocket.close()

if __name__ == "__main__":
    seeder()