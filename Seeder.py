from socket import*

def leecherSend(connectionSocket):
    filename = connectionSocket.recv(1024).decode() # receives the requested file name from the leecher
    print("File to be sent: ", filename) #verifies the correct file to be downloaded
        
    try:
        filename, start, end = filename.split("|")
        start, end = int(start), int(end)

        print ("Sending bytes " + start + " to " + end)
        with open(filename, "rb") as file:
            while chunk := file.read(1024):
                connectionSocket.send(chunk) # sends the file to the leecher in chunks of size 1024 bytes
        print("File sent successfully!") #confirmation message from the seeder
    except FileNotFoundError:
        print("File not found!") # informs leecher the file could not be found
        connectionSocket.send(b"ERROR: File not found")
        
    connectionSocket.close() #closes the socket

def seeder(port, filename):
    serverPort = port #port number for leechers to connect to
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", serverPort))
    serverSocket.listen(1)
    print("The server is ready to send a file")
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Connected to Leecher at: ", addr) # provides information about the leecher currently connected to the seeder
        leecherSend(connectionSocket)

if __name__ == "__main__":
    filename = input("Enter the filename you want to seed: ")
    port = ("Enter the port you would like to use (from 12000 to 12010): ")
    seeder(port, filename) #runs the seeder class