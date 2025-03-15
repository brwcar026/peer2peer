from socket import *
import time
import threading

# Dictionary to store seeder information
# Key: file name, Value: list each seeder info (seeder_ip, seeder_port, last_active_time)
seeders = {}

def trackClient(message, clientAddress, udpSocket):
    #Handles messages from clients (seeders or leechers).
    #Process REGISTER and QUERY messages
    
    modifiedMessage = message.decode().upper()
    
    # Split the message into parts for processing
    splitProtocol = modifiedMessage.split()
    
    if splitProtocol[0] == "REGISTER": # Handle REGISTER message from a seeder
        file = splitProtocol[1]
        seederPort = splitProtocol[2]
        seederIPAdd = clientAddress[0]
    
        if file not in seeders: # Add seeder info to the dictionary
            seeders[file] = []
        seederInfo = {'ip': seederIPAdd, 'port':seederPort, 'Latest Active Time': time.time()}
        seeders[file].append(seederInfo)
        
        # Send confirmation to the seeder
        udpSocket.sendto(b"REGISTERED", clientAddress)
        print (f"{seederPort} {seederIPAdd} has been registered")
    
    elif splitProtocol[0] == "QUERY": # Handle QUERY message from a leecher
        file = splitProtocol[1]
        
        if file in seeders:  # Filter active seeders (last active within 10 minutes)                    
            activeSeeders = []
            for seeder in seeders[file]:
                if (time.time() - seeder['Latest Active Time']) < 600:
                    activeSeeders.append(seeder)
            if activeSeeders == []:
                # No active seeders found
                udpSocket.sendto(b"No_Active_Seeders", clientAddress)
                print(f"No active seeders found for file {file}")
            else:
                # Format: "ip1:port1 ip2:port2 ..."
                seederParts = []                
                for seeder in activeSeeders:
                    seederParts.append(f"{seeder['ip']}:{seeder['port']}")
                seederList = " ".join(seederParts)
                udpSocket.sendto(seederList.encode(), clientAddress)
                print(f"Sent active seeders for file {file} to {clientAddress}: {seederList}") 
                           
        else:
            # File not found in seeders
            udpSocket.sendto(b"File_Not_Found", clientAddress)
            print(f"File {file} not found")   

def tracker(): # Main function for tracker server.
    udp_trackerPort = 12002
    udp_IP = "127.0.0.1"
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind((udp_IP, udp_trackerPort))
    print("The server is ready to track available seeders")
    
    while True:
        message, clientAddress = udpSocket.recvfrom(2048) # Receive messages from clients
        trackerClientThread = threading.Thread(target=trackClient, args=(message, clientAddress, udpSocket))
        trackerClientThread.start()
        
if __name__ == "__main__":
    tracker() # Start the tracker thread