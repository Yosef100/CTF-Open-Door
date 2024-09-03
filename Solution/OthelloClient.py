

import socketio
import requests

# Initialize Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.")

@sio.event
def message(data):
    # Print whatever the server sends
    print(data)
    
    # Check if the message contains "next move"
    if "next move" in data:
        move = input()  # Get the move input from the user
        sio.emit('move', move)  # Send the move to the server

@sio.event
def disconnect():
    print("Disconnected from the server.")

if __name__ == "__main__":
    sio.connect('https://the-open-door.onrender.com/socket.io')
    sio.wait()