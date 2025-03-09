from socket import *
import time
import threading

# Dictionary to store seeder information
# Key: file name, Value: list each seeder info (seeder_ip, seeder_port, last_active_time)
seeders = {}

def trackClient(message, clientAddress, udpSocket):
    modifiedMessage = message.decode().upper()
    #print(f"Received message: {modifiedMessage}")
    
    splitProtocol = modifiedMessage.split()
    
    if splitProtocol[0] == "REGISTER":
        file = splitProtocol[1]
        seederPort = splitProtocol[2]
        seederIPAdd = clientAddress[0]
    
        if file not in seeders:
            seeders[file] = []
        seederInfo = {'ip': seederIPAdd, 'port':seederPort, 'Latest Active Time': time.time()}
        seeders[file].append(seederInfo)
        #print(f"Seeder {seeder_ip}:{seeder_port} registered for file {file_name}")
        udpSocket.sendto(b"REGISTERED", clientAddress)# send a confirmation message to seeder
        print (seederPort + seederIPAdd + " has been registered")
    
    elif splitProtocol[0] == "QUERY":
        file = splitProtocol[1]
        if file in seeders:          
            activeSeeders = []
            for seeder in seeders[file]:
                if (time.time() - seeder['Latest Active Time']) < 60:
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
                
                '''seederList = ",".join([f"{seeder['ip']}:{seeder['port']}" for seeder in activeSeeders])
                udpSocket.sendto(seederList.encode(), clientAddress)
                print(f"Sent active seeders for file {file} to {clientAddress}: {seederList}")''' 
                
                '''activeSeeders = []
                for ip in seeders[file]:
                t = 
                if time.time() - t < 60:
                    active_seeders.append((ip, port, t))
                    seeders[file_name] = active_seeders
            
                seeders[file_name] = [(ip, port, t) for (ip, port, t) in seeders[file_name] if time.time() - t < 60]'''              
                
        else:
            # File not found in seeders
            udpSocket.sendto(b"File_Not_Found", clientAddress)
            print(f"File {file} not found")   

def tracker():
    udp_trackerPort = 12002
    udp_IP = "127.0.0.1"
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind((udp_IP, udp_trackerPort))
    print("The server is ready to track available seeders")
    
    while True:
        message, clientAddress = udpSocket.recvfrom(2048)
        trackerClientThread = threading.Thread(target=trackClient, args=(message, clientAddress, udpSocket))
        trackerClientThread.start()
        #Thread(target=trackClient, args=(message, clientAddress, udpSocket)).start()

if __name__ == "__main__":
    tracker()