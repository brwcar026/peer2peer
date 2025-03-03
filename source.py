import socket
import threading
import os

# Tracker (UDP Server)
def tracker():
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tracker_socket.bind(("localhost", 5000))
    seeders = {}  # Dictionary to store seeder IPs and ports
    print("Tracker is running...")
    
    while True:
        message, addr = tracker_socket.recvfrom(1024)
        message = message.decode()
        if message.startswith("REGISTER"):  # Seeder registration
            _, filename, port = message.split()
            seeders[filename] = (addr[0], int(port))
            tracker_socket.sendto("REGISTERED".encode(), addr)
        elif message.startswith("QUERY"):  # Leecher request
            _, filename = message.split()
            if filename in seeders:
                response = f"SEEDER {seeders[filename][0]} {seeders[filename][1]}"
                tracker_socket.sendto(response.encode(), addr)
            else:
                tracker_socket.sendto("NOT_FOUND".encode(), addr)

# Seeder (TCP Server)
def seeder(filename, port):
    seeder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    seeder_socket.bind(("localhost", port))
    seeder_socket.listen(1)
    
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tracker_socket.sendto(f"REGISTER {filename} {port}".encode(), ("localhost", 5000))
    
    print(f"Seeder is running on port {port} and sharing {filename}...")
    
    while True:
        conn, addr = seeder_socket.accept()
        print(f"Connected to leecher {addr}")
        with open(filename, "rb") as f:
            data = f.read()
            conn.sendall(data)
        conn.close()

# Leecher (TCP Client)
def leecher(filename):
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tracker_socket.sendto(f"QUERY {filename}".encode(), ("localhost", 5000))
    response, _ = tracker_socket.recvfrom(1024)
    response = response.decode()
    
    if response.startswith("SEEDER"):
        _, seeder_ip, seeder_port = response.split()
        seeder_port = int(seeder_port)
        
        leecher_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_socket.connect((seeder_ip, seeder_port))
        
        with open("downloaded_" + filename, "wb") as f:
            data = leecher_socket.recv(1024)
            while data:
                f.write(data)
                data = leecher_socket.recv(1024)
        
        print(f"File {filename} downloaded successfully!")
        leecher_socket.close()
    else:
        print("File not found on tracker.")

# Running the components
if __name__ == "__main__":
    tracker_thread = threading.Thread(target=tracker)
    tracker_thread.start()
    
    seeder_thread = threading.Thread(target=seeder, args=("sample.txt", 6000))
    seeder_thread.start()
    
    leecher_thread = threading.Thread(target=leecher, args=("sample.txt",))
    leecher_thread.start()
