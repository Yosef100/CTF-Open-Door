import socketio

sio = socketio.Client()

import socketio
import json

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.")

@sio.event
def message(data):
    if isinstance(data, dict):
        # Print the received dictionary, formatted as a plain string
        message = data.get('message', '')
        print(message)
        
        # Check if the message contains "next move"
        if "next move" in message:
            move = input()  # Get the move input from the user
            sio.emit('move', {"move": move})  # Send the move to the server

    else:
        # If data is not a dictionary, handle it as a raw string
        try:
            server_data = json.loads(data)
            message = server_data.get('message', '')
            print(message)
            
            # Check if the message contains "next move" after parsing
            if "next move" in message:
                move = input()  # Get the move input from the user
                sio.emit('move', {"move": move})  # Send the move to the server

        except json.JSONDecodeError:
            # If JSON parsing fails, print an error message
            print("Received non-JSON data:", data)
@sio.event
def disconnect():
    print("Disconnected from the server.")



if __name__ == '__main__':
    sio.connect('https://the-open-door.onrender.com/socket.io')
    sio.wait()
