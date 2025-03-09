from socket import *
import threading

from Seeder import seeder

def leecher():
    serverName = "127.0.0.1"  # IP adress for the leecher to connect to 
    serverPort = 12000 #port number for the process of file sharing
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    filename = input("Input the file you want to download: ") # user requests a file to download
    clientSocket.send(filename.encode()) # translates the file name into bytes and sends to the seeders
    
    with open(f"downloaded_{filename}", "wb") as file:
        while chunk := clientSocket.recv(1024): # receives chunks of the fule from the seeder and writes to a new file
            file.write(chunk) 
    
    print("File has been downloaded successfully!") # confirmation message once all chunks have been received
    choice = input("Would you like to become a seeder? (yes/no): ").lower() # asks user if they would like to become a tcp server, converts reply to lower case as well
    if choice == "yes":
        #add code to become a seeder
        #toSeeder()
        seeder_thread = threading.Thread(target = toSeeder)
        seeder_thread.start()
        seeder_thread.join()
    else:
        print("Thank you") 
        clientSocket.close()

def toSeeder():
    new_serverPort = 12001 #port number for leechers to connect to which is different to current port number
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", new_serverPort))
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
    leecher() # runs the leecher class