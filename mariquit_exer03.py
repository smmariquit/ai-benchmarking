# MARIQUIT, SIMONEE EZEKIEL M.
# CMSC 170 Exer 3 - Minimax Algorithm

# Program Description:
# This program utilizes the minimax algorithm to create an AI bot for the tic tac toe game.
# The minimax algorithm, if implemented correctly, will always force a win for its player or a draw.
# The algorithm also uses alpha-beta pruning, which saves unnecessary processing time.
# Pylance was used for type checking, but by no means is this program typesafe xD

# User guide:
# You can set the empty character and the character for the min and max player.
# You can also set your own starting board and AI starting position below

# Limitations
# - All wins or losses have equal value, meaning the minimax algorithm will not differentiate from an immediate win
#   and a win 3 moves later.
# - In the future, I could implement a way for AI to play against AI. It should just be a few lines.

# Responsible use of AI:
# No AI was used in this work

# Used the enum for the list of valid moves para malinis and readable ang code
import enum
import random

# Constants
empty_char = "-"

# X is the maximizing player, O is the minimizing player
class Player(enum.Enum):
    MAX = "X"
    MIN = "O"

class State:
    def __init__(self, board: list, min_or_max: Player, parent_state: 'State', value: int=None, action: int=None):
        self.board = board
        self.min_or_max = min_or_max
        self.value = value
        self.parent_state = parent_state
        self.action = action

moves = {
    0: "1 1", 1: "1 2", 2: "1 3",
    3: "2 1", 4: "2 2", 5: "2 3",
    6: "3 1", 7: "3 2", 8: "3 3"
}

first_move = random.randint(0,8)
# first_move = 0

board = [empty_char] * 9 # initial state of the tic tac toe game
# board = ["Player.MAX.value", "Player.MIN.value", empty_char, 
#           empty_char, "Player.MAX.value", empty_char,
#           empty_char, "Player.MIN.value", empty_char] # for testing purposes

# Global Vars
game_state = State(board, Player.MAX, None)

def print_board(board):
    print("\n",end="  ")
    [print(x, end="") for x in range(1,4)]
    print("\n",end="")
    for i in range(0,3):
        print(i+1,end=" ")
        for j in range(0,3):
            print(board[i*3+j],end="")
        print("\n",end="")
    print("\n",end="")

# Move without needing to prompt the user
def apply_move(node: State, player: Player, move):
    if node.board[move] == empty_char:
        new_board = node.board.copy()
        new_board[move] = player.value
        return State(new_board, Player.MAX if player == Player.MIN else Player.MIN, node)
    else:
        return

# Prompts the user for a move
# Replicates the board entirely, maybe not optimized lol
def prompt_move(node: State, player: Player):
    while True:
        move = input("Make a move, " + player.value + ": (Format: 'row# col#') ")
        if(move not in moves.values()):
            print("Invalid input!")
            continue   
        print("Move:", move)
        i,j = move.split(" ")
        i,j = int(i)-1,int(j)-1
        if node.board[i*3+j] != empty_char:
            print("You tried to move to an occupied space!")
            continue
        new_board = node.board.copy()
        new_board[i*3+j] = player.value
        return State(new_board, Player.MAX if player == Player.MIN else Player.MIN, node)

# Essentially returns all empty squares
def get_valid_moves(board):
    indices = [idx for idx, val in enumerate(board) if val == empty_char]
    return indices

# The core of the minimax algorithm is that a win for the max player is +1 value
# and for the opposite player it's -1
def utility(winner):
    if winner == Player.MAX.value: return 1
    elif winner == Player.MIN.value: return -1
    else: return 0

# The three functions below simulate game tree for the minimax algorithm
def value(node: State, alpha=float('-inf'), beta=float('inf')):
    if winner := check_win(node.board): return utility(winner)
    if is_draw(node.board): return 0
    if node.min_or_max == Player.MAX: return max_value(node, alpha, beta)
    if node.min_or_max == Player.MIN: return min_value(node, alpha, beta)

def max_value(node: State, alpha=float('-inf'), beta=float('inf')):
    m = float('-inf')
    for move in get_valid_moves(node.board):
        new_node = apply_move(node, Player.MAX, move)
        v = value(new_node, alpha, beta)
        m = max(v, m)
        if v >= beta:
            return m  # Alpha-beta cutoff
        alpha = max(m, alpha)
    return m

def min_value(node: State, alpha=float('-inf'), beta=float('inf')):
    m = float('inf')
    for move in get_valid_moves(node.board):
        new_node = apply_move(node, Player.MIN, move)
        v = value(new_node, alpha, beta)
        m = min(v, m)
        if v <= alpha:
            return m  # Alpha-beta cutoff
        beta = min(beta, m)
    return m

# Get the best move given a state
def best_move(node):
    player = node.min_or_max
    nodes = []
    for move in get_valid_moves(node.board): 
        new_node = apply_move(node, player, move)
        v = value(new_node)
        new_node.value = v
        new_node.action = move
        nodes.append(new_node)
    if player == Player.MAX: return max(nodes, key=lambda x: x.value)
    elif player == Player.MIN: return min(nodes, key=lambda x: x.value)

# Check for columns, rows, and diagonals. Return winner or False
def check_win(board):
    for i in range(0,3):
        if (board[i] == board[i+3] == board[i+6]) and board[i] != empty_char: return board[i]
    for i in range(0,3):
        if (board[(i*3)] == board[(i*3)+1] == board[(i*3)+2]) and board[i*3] != empty_char: return board[i*3]
    if board[0] == board[4] == board[8] and board[0] != empty_char: return board[0]
    if board[2] == board[4] == board[6] and board[2] != empty_char: return board[2]
    return False

# Draw if no winners and no more blank spots
def is_draw(board): return is_full(board) and not check_win(board)
def is_full(board): return all([not board[x]==empty_char for x in range(9)])

# Main game functionality

# Prompt the user to ask who plays first
draw = is_draw(game_state.board)
print("[1] AI (" + Player.MAX.value + ")")
print("[2] Me (" + Player.MIN.value + ")")
while True:
    choice = input("Choose who plays first: ")
    if choice not in ["1", "2"]:
        continue
    break

if choice == "1":
    print_board(game_state.board)
    game_state.min_or_max = Player.MAX
    game_state = apply_move(game_state, game_state.min_or_max, first_move)
    print(Player.MAX.value, "played:", moves[first_move])
    game_state.min_or_max = Player.MIN
elif choice == "2":
    game_state.min_or_max = Player.MIN

# Main game loop
while not draw and not check_win(game_state.board):
    print_board(game_state.board)
    if game_state.min_or_max == Player.MAX:
        best = best_move(game_state).action
        print(Player.MAX.value, "played:", moves[best])
        game_state = apply_move(game_state, game_state.min_or_max, best)
    elif game_state.min_or_max == Player.MIN:
        game_state = prompt_move(game_state, game_state.min_or_max)
    draw = is_draw(game_state.board)

# Game over screen
print_board(game_state.board)
if is_draw(game_state.board):
    print("It's a draw!")
else:
    winner = check_win(game_state.board)
    print(winner, "Wins!")    