

I first worked on implementing the logic for the othello game. (in game.py in othello folder) 
The true objective for this game is to form a door shape out of the pieces (details by existsDoor method)
This is hinted at by the emphasis on Open the door - sent every time player is prompted for a move. Additionally, 
after any game where a door was not constructed, the server sends a message hinting towards a door being the true 
objective. Finally, the background picture for the-open-door.onrender.com (also should be found from pcap file) features
a black doorframe filled with white light above which are superimposed (mostly transparent) circles resempling othello
pieces.
The Computer is set to play using an easily identifiable pattern - moves as close to side x as possible where x changes
in a clockwise direction, beginning from top - to help in completing this objective.
A simple solution given the starting board is to perform the moves 44, 38, 76


After that was done, I implemented the server for the website (the-open-door.onrender.com) and the Othello game using Flask
with the waitress production server. I hosted the site on Render.
Since render only allows a single exposed port, using normal sockets would be pointlessly overcomplicated, 
so I researched websockets and implemented the othello server using them instead. The server communicates
using json objects through websockets
The client will need to be written to communicate with the server using json via websockets. This, and other useful details 
are clearly shown on the page /othello-rules, which should be discovered based on the wireshark capture file provided 
in the intro.
An example client may be found in Solution/OthelloClient  (I actually realized the example client  included in my solution
document, was an older version without json. Oh well, it's not really supposed to be in there anyway)
On connection the server creates a board for the client and prompts them for their move. When they disconnect,
their board is removed.
When the server receives a move from the client, it finds the client's board, checks the move for validity,
and if valid executes it. Then the computer takes it's turn.
If after any move the game has been completed, the server sends a message depending on the result and disconnects the client.
If no door was completed, the server sends an appropriate message while hinting towards the true objective not being
the usual win condition for othello.
If a door was completed, a ciphertext message is sent to the client, the plaintext of which is the password for
the-open-door.onrender.com. 

The ciphertext was encrypted using a vigenere cipher with the key "unity". To allow decoding despite the short length,
punctuation, letter case and spacing are all unchanged, and the last sentence of the ciphertext is a phrase with a
distinctiveformat which was repeated several times (after the end of every game and on the page \othello-rules) - 
recognition of which provides known plaintext. 
The encryption algorithm I used is in Solution/vigenereEncrypter.py.
An example decryption algorithm which uses known plaintext to find the key is in Solution/vigenereBreaker.py

Once the text is decrypted it should be entered into the password field on the-open-door.onrender.com. Both the exact
decryption and the decrypted text with punctuation removed are accepted.
Upon the correct password being entered, a PE file masquerading as an image named Open Door will be downloaded. the server
prevents the file from being downloaded prior to this by returning a 403 code if it's attempted by a client who hasn't been
authenticated.
The file is abnormally large for the image size, hinting at it in truth being something else. It is saved in the secure
folder.
When the executable within the file is run it prints a document containing vital intelligence on the Open Door's 
operations.
the file can either be changed to .exe and run (though many systems block it as suspicious activity) or extracted
using the PE header and run on its own.
An example for an extraction algorithm is contained in Solution/PEExtractor.
example extracted files are saved in Solution/Extracted Files

Finally, I created a wireshark capture file on the-open-door.onrender.com's traffic for the intro. As the intro text
specifically mentioned both the name The Open Door and othello, attention should be drawn to the-open-door.onrender.com
as well as the page /othello rules. These pages both contain hints to be used in solving the puzzle, both as to how the 
client to play othello should be constructed, as well as to the game's true objective (and the necessity of finding a 
password)
