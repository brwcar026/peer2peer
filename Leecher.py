import os
from socket import *
import threading
import Seeder

def getSeeders(filename):
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    query = "QUERY " + filename
    udp_socket.sendto(query.encode(), ("127.0.0.1", 12002))

    response, _ = udp_socket.recvfrom(2048)
    udp_socket.close()

    decoded = response.decode()

    if decoded == "No_Active_Seeders":
        print("No seeders sending the file " + filename)
    elif decoded == "File_Not_Found":
        print("The file was not found")
    else:
        allSeeders = decoded.split()
        seeders = [seeder.split(":") for seeder in allSeeders]
        return [(ip ,int(port)) for ip, port in seeders]

def downloadFile(seederIP, seederPort, filename, start, end, chunk_data):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((seederIP, seederPort))
        fileChunk = f"{filename}|{start}|{end}"

        clientSocket.send(fileChunk.encode())

        data = b""
        while True:
            chunk = clientSocket.recv(1024)
            if not chunk:
                break
            data += chunk

        chunk_data.append((start, data))
        print("Successfully downloaded the chunk from the seeder")

    except Exception as e:
        print(f"Could not download from Seeder. {e}")
    finally:
        clientSocket.close()

def leecher(filename):
    seeders = getSeeders(filename)
    if not seeders:
        return
    
    file_size = os.path.getsize(filename)
    numSeeders = len(seeders)
    chunkSize = file_size // numSeeders

    chunkData = []
    threads = []

    for i, (seederIP, seederPort) in enumerate(seeders):
        start = i * chunkSize
        end = start + chunkSize if  i < numSeeders - 1 else file_size

        thread = threading.Thread(target = downloadFile, args = (seederIP, seederPort, filename, start, end, chunkData)) 
        threads.append(thread)
        thread.start()

    for i in threads:
        thread.join()

    chunkData.sort()
    
    with open(f"downloaded_{filename}", "wb") as file:
        for _, data in chunkData:
            file.write(data)
    
        print("File has been downloaded successfully!") # confirmation message once all chunks have been received

    choice = input("Would you like to become a seeder? (yes/no): ").lower() # asks user if they would like to become a tcp server, converts reply to lower case as well
    
    if choice == "yes":
        #add code to become a seeder
        #filename = input("Enter the filename you want to seed: ")
        new_port = input("Enter the port you would like to use (from 12002): ")
        Seeder.connectToTracker(filename, int(new_port))
        Seeder.seeder(int(new_port), filename)
    else:
        print("Thank you") 
        

if __name__ == "__main__":
    filename = input("Input the file you want to download: ") # user requests a file to download
    leecher(filename) # runs the leecher class