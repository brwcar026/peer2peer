import socket
# Registers the Seeder with the Tracker
def connectToTracker(filename, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    # Format: "REGISTER <filename> <port>"
    register = "REGISTER " + filename + " " + str(port) #sends a message to the tracker saying the seeder wishes to be tracked
    udp_socket.sendto(register.encode(), ("127.0.0.1", 12002))

    response, _ = udp_socket.recvfrom(2048)
    decoded = response.decode()

    if decoded == "REGISTERED": #if there was a positive confirmation, print so on the seeder side, if not, print an error message
        print("Successfully registered with tracker")
    else:
        print("Could not register with tracker")

    udp_socket.close() #closes the udp socket


# Sends the requested file chunk to the Leecher
def leecherSend(connectionSocket):
    filename = connectionSocket.recv(1024).decode() # receives the requested file name from the leecher
    print("File to be sent: " + filename) #verifies the correct file to be downloaded
        
    try:
        # filename and byte range
        filename, start, end = filename.split("|")
        start, end = int(start), int(end)

        print (f"Sending bytes {start} to {end}") #clarifies which byte of the file the seeder is sending

        #Read and send the file chunk
        with open(filename, "rb") as file:
            file.seek(start)
            chunk = file.read(end - start)
            connectionSocket.sendall(chunk) # sends the file to the leecher in chunks of size 1024 bytes

            print("File chunk sent successfully!") #confirmation message from the seeder

    except FileNotFoundError:
        print("File not found!") # informs leecher the file could not be found
        connectionSocket.send(b"ERROR: File not found")
    finally:
        connectionSocket.close() #closes the socket

# Main fuunction for the Seeder. Listens for incoming connections from Leechers.
def seeder(port, filename):
    serverPort = port #port number for leechers to connect to
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", serverPort))
    serverSocket.listen(1)
    print(f"The server is ready to send " + filename + " on port " + str(port))
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Connected to Leecher at: ", addr) # provides information about the leecher currently connected to the seeder
        leecherSend(connectionSocket)

if __name__ == "__main__":
    filename = input("Enter the filename you want to seed: ")
    port = input("Enter the port you would like to use (from 12002): ")
    connectToTracker(filename, int(port)) # connects to the tracker
    seeder(int(port), filename) #runs the seeder class
    