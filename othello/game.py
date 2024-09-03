import copy
EMPTY, BLACK, WHITE = '.', '○', '●'
HUMAN, COMPUTER = '●', '○'

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)


'''
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. (human) turn number
2. Who's turn is it: HUMAN or COMPUTER
3. flag if door exists

'''


def isHumTurn(s):
#Returns True iff it the human's turn to play
    return s[2]==HUMAN

def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


def create():
    global HUMAN,COMPUTER
    board = [EMPTY] * 100
    initial = [
    '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '●', '○', '○', '○', '.', '.',
    '.', '●', '○', '●', '●', '○', '○', '.',
    '.', '.', '○', '.', '○', '●', '.', '.',
    '.', '●', '○', '●', '●', '●', '○', '.',
    '.', '.', '○', '●', '●', '○', '●', '.',
    '.', '.', '.', '.', '○', '.', '.', '.',
    '.', '.', '.', '.', '●', '.', '.', '.'
]
    k=0
    for i in squares():
        board[i] = initial[k]
        k+=1

    return [board,0 , HUMAN,False]

def printState(s):
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(s[0][begin:end]))
    print(rep)
    return rep

def requestMove(s):
    response = ""
    response += printState(s)
    response += "To make your move enter a two digits number, the first number is row and the second is column" "\n" \
    "For example: if you want to choose the first row and the third column enter 13" "\n"\
    "The door must be opened" "\n"\
    ". Enter your next move: " 
    return response

def inputMove(move, s):
 # Reads, enforces legality, and executes the user's move.
    response = ""
    try:
        move = int(move)
    except Exception as e:
        return "illegal input"
    
    if isLegal(move, s) == False:        
        response += "Illegal move.\n"
    else:
        makeMove(move, s)
        s[1] += 1
        response += f"Move made at position {move}.\n"
    return response

#calculate computer's move. Furthest in x direction, with x moving clockwise, starts at UP
def compMove(s):
    moves = legalMoves(s)
    if len(moves) == 0:
        return "no legal moves"
    # Determine sorting criteria based on the move count
    if s[1] % 4 == 0:
        moves.sort(key=lambda i: i % 10)  # Sort by column (leftmost)
    elif s[1] % 4 == 1:
        moves.sort(key=lambda i: i // 10)  # Sort by row (topmost)
    elif s[1] % 4 == 2:
        moves.sort(key=lambda i: i % 10, reverse=True)  # Sort by column (rightmost)
    elif s[1] % 4 == 3:
        moves.sort(key=lambda i: i // 10, reverse=True)  # Sort by row (bottommost)
    
    makeMove(moves[0], s)
    return moves[0]
    
'''check if a door exists on the board. a door is an all white rectangle with a line of black 
pieces on all sides but the bottom, who's centered on the board's center (rect with even sides
centered on center), h >= w, min h/w = 4,2
'''
def existsDoor(s):
    board = s[0]
    # Center of the board is next to index 54 (5th row, 5th column on a 1-based index).
    center = 54
    
    # Define valid sizes: (height, width) min is 4,2. height>=width, h,w %2 == 0 
    valid_sizes = [(4, 2), (4,4), (5,4), (6,2), (6,4), (6,6)]  # Adjust this list as needed
    
    
    for height, width in valid_sizes:
        # Calculate offsets for the top-left corner of the rectangle (of the border - doorframe)
        top_left = center - (height // 2) * DOWN - (width // 2) + UP
        
        # Initialize flag to determine if the door pattern is valid
        valid_pattern = True
        
        # Check the black border on top and sides
        for i in range(width+2):
            if board[top_left + i] != BLACK:  # Top border
                valid_pattern = False
                break
        for i in range(1, height+1):  # Left and right borders
            if board[top_left + i * DOWN] != BLACK or board[top_left + i * DOWN + (width + 1)] != BLACK:
                valid_pattern = False
                break

        # Check the white interior
        for i in range(1, height+1):
            for j in range(1, width+1):
                if board[top_left + i * DOWN + j] != WHITE:
                    valid_pattern = False
                    break
        
        # If the pattern is found, return True
        if valid_pattern:
            return True
    
    # If no valid pattern is found, return False
    return False

#check if the game is over 
def isFinished(s):
    fin = False
    #if a door has been completed
    if existsDoor(s):
        s[3] = True
        return True
    #if there's no legal moves for current player
    if (not(anyLegalMove(s))):
        #save who's turn it is now
        if (s[2] == HUMAN):
            other = COMPUTER
            current = HUMAN
        else:
            other = HUMAN
            current = COMPUTER
        #switch to other player and check for any legal moves
        s[2] = other
        #if there's no legal moves for other player as well, game is over
        if (not(anyLegalMove(s))):
            return True           
        s[2] = current #restore turn
    
    return fin


def isLegal(move, s):
    hasbracket = lambda direction: findBracket(move, s, direction)    
    return (s[0][move] == EMPTY) and (any(map(hasbracket, DIRECTIONS)))

# get a list of legal moves for the player
def legalMoves(s):
    return [sq for sq in squares() if isLegal(sq, s)]

# Is there any legal move for this player
def anyLegalMove(s):
    isAny = any(isLegal(sq, s) for sq in squares())
    return isAny

def makeFlips(move, s, direction):
    bracket = findBracket(move, s, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        s[0][square] = s[2]
        square += direction

def changePlayer(s):
    if s[2] == COMPUTER:
        s[2] = HUMAN
    else:
        s[2] = COMPUTER

def makeMove(move, s):
    s[0][move] = s[2]
    for d in DIRECTIONS:
        makeFlips(move, s, d)
    changePlayer (s)
    return s

def whoWin (s):
    computerScore=0
    humanScore=0
    for sq in squares():
        piece = s[0][sq]
        if piece == COMPUTER:
            computerScore += 1
        elif piece == HUMAN:
            humanScore += 1
    if (computerScore>humanScore):
        return COMPUTER

    elif (computerScore<humanScore):
        return HUMAN

    return 0.00001 #not 0 because TIE is 0


def isValid(move):
    return isinstance(move, int) and move in squares()

def findBracket(square, s, direction):
    bracket = square + direction
    if bracket // 10 < 1 or bracket% 10 == 9 or bracket% 10 == 0:  # Check if bracket is within bounds
        return None
    if s[0][bracket] == s[2]:
        return None
    opp = BLACK if s[2] is WHITE else WHITE
    while s[0][bracket] == opp:
        bracket += direction
        if bracket // 10 < 1 or bracket% 10 == 9 or bracket% 10 == 0:  # Check if bracket is within bounds
            return None
    return None if s[0][bracket] in (EMPTY) else bracket

