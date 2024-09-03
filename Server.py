import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory, abort, session, flash
from flask_socketio import SocketIO, disconnect, emit
import os
import waitress
import othello.game as game

ENCRYPTED_MESSAGE = "Eawpjyqox kofb uc zemx, uy jqej gnsx gn fw. Lnlriw ri nte zyamtrb gpx qel. Cgtyvt mfy Gznrb, Hvecufp mfy vvyghvbx!"

CORRECT_PASSWORD = ["Knowledge must be free, we will make it so. Spread to all beneath the sky. Unveil the Truth, Unleash the infinite!",
                    "Knowledge must be free we will make it so spread to all beneath the sky Unveil the Truth Unleash the infinite"]

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.secret_key = 'fsrg6uUDYHhuhg65EBEe' 
socketio = SocketIO(app)

# Global dictionary to store game boards for each client
clients_boards = {}

app.static_folder = 'static'
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")
        if password in CORRECT_PASSWORD:
            session['authenticated'] = True  # Mark the user as authenticated
            return render_template("success.html")  # Render success page
        else:
            flash("Incorrect password. Please try again.")  # Show error message
            return render_template("index.html")
    
    return render_template("index.html")

@app.route("/download")
def download():
    if session.get('authenticated'):  # Check if the user is authenticated
        return send_from_directory(directory='./secure', path='Open Door.png', as_attachment=True)
    else:
        abort(403)  # Forbidden if accessed directly

@app.route("/expire_session")
def expire_session():
    session.clear()  # Clear the session
    return redirect(url_for('index'))  # Redirect to the index page

@app.route("/othello-rules")
def othello_rules():
    return render_template("othello_rules.html")

@app.route("/health")
def health_check():
    return "OK", 200

@socketio.on('connect')
def handle_connect():
    print("Client connected.")
    # Create a new game board for the connected client
    board = game.create()
    clients_boards[request.sid] = board
    
    emit('message', {"message": "Welcome back to Open Door Othello. You are WHITE:"})
    # Send the initial board and request a move from the client
    emit('message', {"message": game.requestMove(board)})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected.")
    # Remove the client's board when they disconnect
    if request.sid in clients_boards:
        del clients_boards[request.sid]

@socketio.on('move')
def handle_move(data):
    # Ensure the data is in JSON format
    if isinstance(data, str):
        try:
            # Attempt to parse JSON
            move_data = json.loads(data)
        except json.JSONDecodeError:
            # If JSON parsing fails, return an error message
            emit('message', {"message": "Error: Invalid JSON format."})
            return
    else:
        move_data = data
    
    # Get the move from the JSON data
    move = move_data.get("move")
    
    if request.sid not in clients_boards:
        emit('message', {"message": "Error: Game not initialized."})
        return

    # Get the board associated with the current client
    board = clients_boards[request.sid]

    # Process the player's move
    move = str(move)  # Ensure move is a string before passing it
    response = game.inputMove(move, board)
    emit('message', {"message": response})

    # Check if there are any legal moves left for the current player
    if not game.anyLegalMove(board):
        emit('message', {"message": f"Player {board[2]}: No more moves. Changing player.\n"})
        game.changePlayer(board)
        
    # If the game isn't over
    if not game.isFinished(board):    
        if not game.isHumTurn(board):
            # Computer makes its move
            computer_move = game.compMove(board)
            emit('message', {"message": f"Computer's move: {computer_move}"})
     
    # If the game isn't over
    if not game.isFinished(board):       
        # Send the updated board state after the computer's move
        emit('message', {"message": game.requestMove(board)})
    
    else:
        emit('message', {"message": game.printState(board)})
        # Handle the end of the game
        if board[3]:  # Check if the board represents an "open door"
            emit('message', {"message": "The door is open. The knowledge you seek is yours. Congrats comrade. Unveil the Truth, Unleash the infinite!"})
            emit('message', {"message": ENCRYPTED_MESSAGE})
        else:
            winner = game.whoWin(board)
            if winner == game.COMPUTER:
                emit('message', {"message": "Too bad. But are you sure you're on the path to what you seek? Do it right this time comrade. Unveil the Truth, Unleash the infinite!"})
            elif winner == game.HUMAN:
                emit('message', {"message": "Nice one! But the door has not opened to you... Are you sure you're on the path to what you seek? Do it right this time comrade. Unveil the Truth, Unleash the infinite!"})
            else:
                emit('message', {"message": "It's a tie. Are you sure you're on the path to what you seek? Do it right this time comrade. Unveil the Truth, Unleash the infinite!"})

        # Disconnect the client
        emit('message', {"message": "Disconnecting..."})
        disconnect()       

def start_server():
    # Start Flask app with Waitress
    port = int(os.environ.get("PORT", 10000))
    waitress.serve(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start_server()