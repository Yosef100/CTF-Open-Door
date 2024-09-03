from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory, abort, session, flash
from flask_socketio import SocketIO, emit
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
    
    # Send the initial board and request a move from the client
    emit('message', game.requestMove(board))

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected.")
    # Remove the client's board when they disconnect
    if request.sid in clients_boards:
        del clients_boards[request.sid]

@socketio.on('move')
def handle_move(move):
    if request.sid not in clients_boards:
        emit('message', "Error: Game not initialized.")
        return

    # Get the board associated with the current client
    board = clients_boards[request.sid]

    # Process the player's move
    response = game.inputMove(move, board)
    emit('message', response)

    # Check if there are any legal moves left for the current player
    if not game.anyLegalMove(board):
        emit('message', f"Player {board[2]}: No more moves. Changing player.\n")
        game.changePlayer(board)
        
    #if game isn't over
    if not game.isFinished(board):    
        if not game.isHumTurn(board):
            # Computer makes its move
            computer_move = game.compMove(board)
            emit('message', f"Computer's move: {computer_move}")
     
    #if game isn't over
    if not game.isFinished(board):       
        # Send the updated board state after the computer's move
        emit('message', game.requestMove(board))
    
    else:
        emit('message', game.printState(board))
        # Handle the end of the game
        if board[3]:
            emit('message', "The door is open. The knowledge you seek is yours. Congrats comrade. Unveil the Truth, Unleash the infinite!")
            emit('message', ENCRYPTED_MESSAGE)
        else:
            winner = game.whoWin(board)
            if winner == game.COMPUTER:
                emit('message', "Too bad. But are you sure you're on the path to what you seek? Do it right this time comrade. Unveil the Truth, Unleash the infinite!")
            elif winner == game.HUMAN:
                emit('message', "Nice one! But the door has not opened to you... Are you sure you're on the path to what you seek? Do it right this time comrade. Unveil the Truth, Unleash the infinite!")
            else:
                emit('message', "It's a tie. Are you sure you're on the path to what you seek? Do it right this time comrade. Unveil the Truth, Unleash the infinite!")

def start_server():
    # Start Flask app with Waitress
    port = int(os.environ.get("PORT", 10000))
    waitress.serve(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start_server()