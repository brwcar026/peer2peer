from socket import *

def leecher():
    serverName = "127.0.0.1"  
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    filename = input("Input the file you want to download: ")
    clientSocket.send(filename.encode())
    
    with open(f"downloaded_{filename}", "wb") as file:
        while chunk := clientSocket.recv(1024):
            file.write(chunk)
    
    print("File has been downloaded successfully!")
    choice = input("Would you like to become a seeder? (yes/no): ")
    clientSocket.close()

if __name__ == "__main__":
    leecher()