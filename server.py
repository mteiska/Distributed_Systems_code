import socket
from threading import Thread
import time

from pip import main


SERVER_PORT = 5002 # Port to open server with
SERVER_HOST = "0.0.0.0" #Server uses this as IP
separator_token = ":" #separating CLIENT from msg
users = {}
ch1 = []
ch2 = []
ch3 = []

client_sockets = set() #unordered set for connections later

s = socket.socket() #create socket 

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #setting options for socket to use TCP IPPROTO_TCP is option SO_REUSEADDR to reuse local addresses

s.bind((SERVER_HOST, SERVER_PORT)) #bind to socket so we can receive messages aswell.
print(f"Trying to listen server {SERVER_HOST}:{SERVER_PORT}")
s.listen(5) #wait for connection to binded server socket.

def broadcast(message):
    for client_socket in client_sockets:
        client_socket.send(message.encode())

def send_msg_ch1(msg):
    for client in ch1:
        client.send(msg.encode())


# Sends received messages to clients in channel 2
def send_msg_ch2(msg):
    for client in ch2:
        client.send(msg.encode())


# Sends received messages to clients in channel 3
def send_msg_ch3(msg):
    for client in ch3:
        client.send(msg.encode())

def listen_clients(client_socket):
    try:
        while True:
            time.sleep(1)
           
                #continious listening for socket
                #WIP: create channels and add user to one channel and remove from another
            message = client_socket.recv(1024).decode()
            # Switching users to channel 1 and removing from other channels
            if 'ch1' in message:
                if client_socket not in ch1:
                    ch1.append(client_socket)      # Add to channel
                    if client_socket in ch2:
                        ch2.remove(client_socket)  # Remove from other channels
                    elif client_socket in ch3:
                        ch3.remove(client_socket)
                    
                    client_socket.send("Switched to channel 1.".encode('utf-8'))
                    continue
    
                # Switching users to channel 2 and removing from other channels.
            elif 'ch2' in message:
                if client_socket not in ch2:
                    ch2.append(client_socket)      # Add to channel
                    if client_socket in ch1:
                        ch1.remove(client_socket)  # Remove from other channels
                    elif client_socket in ch3:
                        ch3.remove(client_socket)
                    
                    client_socket.send("Switched to channel 2.".encode('utf-8'))
                    continue
    
            # Switching users to channel 3 and removing from other channels.
            elif 'ch3' in message:
                if client_socket not in ch3:
                    ch3.append(client_socket)      # Add to channel
                    if client_socket in ch1:
                        ch1.remove(client_socket)  # Remove from other channels
                    elif client_socket in ch2:
                        ch2.remove(client_socket)
                    
                    client_socket.send("Switched to channel 3.".encode('utf-8'))
                    continue
    
            # Leave both channels
            elif 'main' in message:
                if client_socket in ch1:
                    ch1.remove(client_socket)
                if client_socket in ch2:
                    ch2.remove(client_socket)
                if client_socket in ch3:
                    ch3.remove(client_socket)
                client_socket.send("User left channels.".encode('utf-8'))
    
            elif 'disconnect' in message:
                client_sockets.remove(client_socket)
                client_socket.close()
                for key,value in users.items():
                    
                    if value == client_socket:
                        deletable = users[key]
                        
                del deletable
                        
                break
    
    
            elif message.startswith("#"):

                users[message[1:].lower()]=client_socket
            
            elif message.startswith("@"):
                users[message[1:message.index(':')].lower()].send(message[message.index(':')+1:].encode())
            else:
                    if client_socket in ch1:
                        send_msg_ch1(message)
                    elif client_socket in ch2:
                        send_msg_ch2(message)
                    elif client_socket in ch3:
                        send_msg_ch3(message)
                    #This is for sending message to all clients
                    else:
                        broadcast(message)
    
    
    except Exception as e:
            #If Exception then client no longer connected so remove it from set
        print("Error: ", e)
        client_sockets.remove(client_socket)
        pass
        
if __name__ == "__main__":
  while True:
  
      # Listen for new connections
      client_socket, client_address = s.accept()
      print(f" New user: {client_address} connected.")
      # add to clients list.
      client_sockets.add(client_socket)
      # start a new thread that listens for each client's messages
      
      thread = Thread(target=listen_clients, args=(client_socket,)) #create thread to listen for clients and receiveing their message. 
      # if main thread ends so do all client threads so set them as deamon since "The daemon process will continue to run as long as the main process 
      # is executing and it will terminate after finishing its execution or when the main program would be killed."
      thread.daemon = True
      # start the thread
      thread.start()
