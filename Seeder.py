from socket import*

def seeder():
    serverPort = 12000 #port number for leechers to connect to
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", serverPort))
    serverSocket.listen(1)
    print("The server is ready to send a file")
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Connected to Leecher at: ", addr) # provides information about the leecher currently connected to the seeder
        filename = connectionSocket.recv(1024).decode() # receives the requested file name from the leecher
        print("File to be sent: ", filename) #verifies the correct file to be downloaded
        
        try:
            with open(filename, "rb") as file:
                while chunk := file.read(1024):
                    connectionSocket.send(chunk) # sends the file to the leecher in chunks of size 1024 bytes
            print("File sent successfully!") #confirmation message from the seeder
        except FileNotFoundError:
            print("File not found!") # informs leecher the file could not be found
            connectionSocket.send(b"ERROR: File not found")
        
        connectionSocket.close() #closes the socket

if __name__ == "__main__":
    seeder() #runs the leecher class