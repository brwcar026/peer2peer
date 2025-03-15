import os
from socket import *
import threading
import Seeder
#imports to create the gui 
from tkinter import * 
from tkinter.ttk import *

#create the window with title "Download Porgress" and a horizontal progress bar 
root = Tk()
root.title("Download Progress")
bar = Progressbar(root, orient= HORIZONTAL, length = 300, mode= "determinate")

def getSeeders(filename): #method to receive the list of seeders from the tracker
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    query = "QUERY " + filename
    udp_socket.sendto(query.encode(), ("127.0.0.1", 12002)) #sends a query to find all available trackers for the file requested

    response, _ = udp_socket.recvfrom(2048)
    udp_socket.close()

    decoded = response.decode() #decodes the response from the tracker
    # if no seeders are sending the file, the program prints there are no seeders
    if decoded == "No_Active_Seeders":
        print("No seeders sending the file " + filename)
    #if the file was not found, the program prints a message saying so
    elif decoded == "File_Not_Found":
        print("The file was not found")
    else:
        #gets all the seeders available for the file
        allSeeders = decoded.split()
        seeders = [seeder.split(":") for seeder in allSeeders]
        return [(ip ,int(port)) for ip, port in seeders]

#method downloads the file from all seeders available
def downloadFile(seederIP, seederPort, filename, start, end, chunk_data, file_size):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((seederIP, seederPort))
        fileChunk = f"{filename}|{start}|{end}" #sends the chunk of data the seeder should send

        clientSocket.send(fileChunk.encode())

        # starts a data variable that is an empty byte
        data = b""
        while True:
            chunk = clientSocket.recv(1024)
            if not chunk:
                break
            data += chunk # appends the data with the chunk received

        chunk_data.append((start, data))
        print("Successfully downloaded the chunk from the seeder")

    except Exception as e:
        print(f"Could not download from Seeder. {e}") # prints the error message if chunk could not be sent
    finally:
        clientSocket.close()

# main method for the leecher
def leecher(filename):
    seeders = getSeeders(filename) #gets seeders sending the filename from the tracker
    if not seeders: # if empty, return
        return
    
    file_size = os.path.getsize(filename) #gets the filesize of the file
    numSeeders = len(seeders) 
    chunkSize = file_size // numSeeders # splits the file into chunks based on how many seeders are sending the file

    chunkData = []
    threads = []

    #this section downloads the file from the seeders 
    for i, (seederIP, seederPort) in enumerate(seeders):
        start = i * chunkSize
        end = start + chunkSize if  i < numSeeders - 1 else file_size

        thread = threading.Thread(target = downloadFile, args = (seederIP, seederPort, filename, start, end, chunkData, file_size)) 
        threads.append(thread)
        thread.start()
        
        bar["value"] = (end / file_size) * 100 #set the percentage to the end segment of the chunk being downloaded 
        root.update_idletasks() #update the progress bar to reflect the amount of chunks that have been downloaded
        
    for i in threads:
        thread.join()

    chunkData.sort() #sorts the data into the correct order
    
    with open(f"downloaded_{filename}", "wb") as file:
        for _, data in chunkData:
            file.write(data) #writes the downloaded chunks into a new file 
    
        print("File has been downloaded successfully!") # confirmation message once all chunks have been received
        
    choice = input("Would you like to become a seeder? (yes/no): ").lower() # asks user if they would like to become a tcp server, converts reply to lower case as well
    
    if choice == "yes":
        root.destroy() #destroys the loading bar as quit seemed to stall too long
        new_port = input("Enter the port you would like to use (from 12002): ") #user chooses a new port number to send the file just downloaded to a new seeder
        Seeder.connectToTracker(filename, int(new_port)) # registers as seeder with tracker
        Seeder.seeder(int(new_port), filename) #starts the seeder method
        
    else:
        print("Thank you") 

bar.pack(pady = 10) # pack the loading bar into the main window

if __name__ == "__main__":
    filename = input("Input the file you want to download: ") # user requests a file to download
    leecher(filename) # runs the leecher class
