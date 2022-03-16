
from threading import Thread
import socket

# server's IP address

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = ":" # Separator for name and msg

# Create the TCP Socket for client
s = socket.socket()
print(f"Trying to connect to:  {SERVER_HOST}:{SERVER_PORT}")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("Connection succesful.")
# Ask client for nickname
nickname = input("Enter your name: (prefix with '#')")
s.send(nickname.encode())
print("Type ch1,ch2,ch3,main to change to corresponding channel.")
print("Type 'disconnect' to disconnect from server.")
def message_listener():

    while True:
        message = s.recv(1024).decode()
       
        print("\n" + message)


# make a thread that listens for messages to this client & print them
t = Thread(target=message_listener)
# Again lets create daemon thread so it ends when main process ends according to same principle used in server side.
t.daemon = True
# start the thread
t.start()
print("If you want to message other users start with @user:message")
while True:
    # input message we want to send to the server
    msg_to_send =  input()
    # a way to exit the program
    if msg_to_send.lower() == 'disconnect':
        s.send("disconnect".encode())
        break
    if msg_to_send.startswith("@"):
        s.send(msg_to_send.encode())
    else:
        to_send = f"{nickname[1:]}{separator_token}{msg_to_send}" #send
        # finally, send the message
        s.send(to_send.encode())

s.close()  # close socket once 'disconnect' message has been send.
