from socket import*

def seeder():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", serverPort))
    serverSocket.listen(1)
    print("The server is ready to send a file")
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Connected to Leecher at: ", addr)
        filename = connectionSocket.recv(1024).decode()
        print("File to be sent: ", filename)
        
        try:
            with open(filename, "rb") as file:
                while chunk := file.read(1024):
                    connectionSocket.send(chunk)
            print("File sent successfully!")
        except FileNotFoundError:
            print("File not found!")
            connectionSocket.send(b"ERROR: File not found")
        
        connectionSocket.close()

if __name__ == "__main__":
    seeder()