# MARIQUIT, SIMONEE EZEKIEL M.
# CMSC 170 Exer 2 - Solving the 8-Puzzle with Informed Search Strategies
# Search trees allow AI algorithms to brute force search the entire state space of a game and find the way to solve it.
# In this program, we use Breadth First Search and Depth First Search to get the solution to an 8-puzzle game.

# Limitations:
# - Standard A* should check if a successor is already in the frontier with a higher cost before adding i
# - Lists are a bit inefficient for an explored state. Can convert the board state to an int and put inside a set
#   (just learned that you can't put lists inside sets!) or use tuples. But it works.
# - Can add a timeout to see if the DFS is going in an infinite loop
# - When the puzzle is unsolvable, BFS can be made to determine that it has explored all possible states, although this is out of scope
# - Can make the file name to use based on user input
# - Not very optimized lol, can use sets (O(1)) when possible, save data used multiple times as arrays

# Nice features:
# - You can change the solved state and the program will work just fine
# - This uses a single array as opposed to a 3x3 one. I find that it makes the array operations a bit more intuitive.
#   - Left: i-1
#   - Right: i+1
#   - Up: i-3
#   - Down: i+3
#   - X-distance: (j - i) % 3
#   - Y-distance: (j - i) // 3

# Responsible use of AI:
# No AI was used in this work

# User guide:
# To use, change the following text file "puzzle.txt" to the desired board state.
# The file should contain 3 lines, each line containing 3 numbers separated by semicolons, for example:
#   1;2;3
#   4;5;6
#   7;8;0

# Addl info:
# One cool thing about the 8-puzzle is that it's one of the few games with a relatively small state space that fits in memory.

def getBoard(board, filename):
    with open(filename, "r") as file: 
        for x in file.read().split("\n"):
            board += [int(i) for i in x.split(";") if i != ""]
    
board = []

# Used the enum for the list of valid moves para malinis and readable ang code
import enum
# Optimized priority queue for astar https://docs.python.org/3/library/heapq.html#module-heapq
import heapq
# Itertools is currently used for tiebreaking mechanism of the priority queue https://docs.python.org/3/library/itertools.html#module-itertools
import itertools

# Valid moves enum
class Moves(enum.Enum): 
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"

class Solutions(enum.Enum):
    BFS = "Breadth First Search"
    DFS = "Depth First Search"
    ASTAR = "A* Search"

class Heuristics(enum.Enum):
    H1 = "Misplaced Tiles"
    H2 = "Manhattan Distance"
    H3 = "Non-adjacent Tiles"

# The solved state of the 8-puzzle  
SOLVED_STATE = [1,2,3,
          4,5,6,
          7,8,0]

# Neighbors without duplicates on a 9x9 grid based on 0-indexing
# If we used a 3x3 array, neighbor checking would just be -1 or +1 hahaha
NEIGHBORS = {
    0: [1],
    1: [2,4],
    2: [5],
    3: [0,4,6],
    4: [5,7],
    5: [8],
    6: [7],
    7: [8],
    # 8: none,
}

ADJACENCIES_3X3 = 12

# No need for this if the solved state is also the zero-indexed 8-puzzle. This is for the 8-puzzle where 0 is at the bottom right.
goal_adj_tiles = [(0,1), (1,2), (3,4), (4,5), (6,7), (7,8), (0,3), (1,4), (2,5), (3,6), (4,7), (5,8)]


# State class, annotated the data para malinaw
class State:
    def __init__(self, board: list, idx: int, action: Moves, parent_state: 'State', cost: int=0, h1: int = None, h2: int = None, h3: int = None):
        self.board = board
        self.idx = idx
        self.action = action
        self.parent_state = parent_state
        self.cost = parent_state.cost + 1 if parent_state else 0
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3

    def n_misplaced_tiles(self):
        misplaced_tiles = 0
        for i in range(0,9):
            if self.board[i] != SOLVED_STATE[i] and self.board[i] != 0:
                misplaced_tiles = misplaced_tiles + 1
        self.h1 = misplaced_tiles

    def manhattan_distance(self):
        manhattan_distance = 0
        for i in range(0,9):
            x_distance = (abs(self.board.index(i) - SOLVED_STATE.index(i))) % 3
            y_distance = (abs(self.board.index(i) - SOLVED_STATE.index(i))) // 3
            manhattan_distance = manhattan_distance + x_distance + y_distance
        self.h2 = manhattan_distance

    def adjacent_tiles(self):
        adjacent_tiles = []
        for i in NEIGHBORS.keys():
            for j in NEIGHBORS[i]:
                adjacent_tiles.append((self.board[i], self.board[j]))
        matches = list(set(adjacent_tiles) & set(goal_adj_tiles))
        num_matches = len(matches)
        non_adjacent_tiles = ADJACENCIES_3X3 - num_matches   
        self.h3 = non_adjacent_tiles

# Define a queue and stack data structure for readability
class Queue:
    def __init__(self, data: list):
        self.data = data
    
    def enqueue(self, key):
        self.data.append(key)
    
    def dequeue(self):
        return self.data.pop(0)

class Stack:
    def __init__(self, data: list):
        self.data = data
    
    def push(self, key):
        self.data.append(key)
    
    def pop(self):
        return self.data.pop()

# Reference: https://www.geeksforgeeks.org/dsa/check-instance-8-puzzle-solvable/\
# (loose) DEFINITION: An inversion is a reverse order of appearance of two numbers compared to the solved state
# THEOREM: if the number inversions in an 8-puzzle is odd, it is unsolvable
def get_inv_count(arr):
    inv_count = 0
    empty_value = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def is_solvable(arr): return True if get_inv_count(arr) % 2 == 0 else False

def print_board(board):
    print("\n",end="")
    for i in range(0,3):
        for j in range(0,3):
            print(board[i*3+j],end=" ")
        print("\n",end="")
    print("\n",end="")

# Use a queue for the minimization functionality
def solve_astar(board, heuristic):
    initial_state = State(board, board.index(0), None, None)
    solve_dto = {}
    counter = itertools.count()
    explored = []
    frontier = []
    if heuristic == Heuristics.H1:
        initial_state.n_misplaced_tiles()
        f = initial_state.h1 + initial_state.cost
    if heuristic == Heuristics.H2:
        initial_state.manhattan_distance()
        f = initial_state.h2 + initial_state.cost
    if heuristic == Heuristics.H3:
        initial_state.adjacent_tiles()
        f = initial_state.h3 + initial_state.cost
    # in heapq, you can put 3 things in the list to make sure that if there are ties, it will use the next thing to compare https://docs.python.org/3/library/heapq.html#module-heapq
    heapq.heappush(frontier, (f, next(counter), initial_state))
    while frontier:
        current_state_tuple = heapq.heappop(frontier)
        current_state = current_state_tuple[2]
        if current_state.board in explored:
            continue
        explored.append(current_state.board)
        if current_state.board == SOLVED_STATE:
            solve_dto["solved_state"] = current_state
            solve_dto["explored_states"] = explored
            return solve_dto
        for valid_move in get_valid_moves(current_state.board):
            new_board = move(current_state.board, valid_move)
            if new_board in explored:
                continue
            idx = new_board.index(0)
            new_state = State(new_board, new_board.index(0), valid_move, current_state)
            if heuristic == Heuristics.H1:
                new_state.n_misplaced_tiles()
                f = new_state.h1 + new_state.cost
            if heuristic == Heuristics.H2:
                new_state.manhattan_distance()
                f = new_state.h2 + new_state.cost
            if heuristic == Heuristics.H3:
                new_state.adjacent_tiles()
                f = new_state.h3 + new_state.cost
            heapq.heappush(frontier, (f, next(counter), new_state))
    return None

def solve_bfs(board):
    initial_state = State(board, board.index(0), None, None)
    solve_dto = {}
    explored = []
    frontier = Queue([initial_state])
    while frontier.data:
        current_state = frontier.dequeue()
        if current_state.board in explored:
            continue
        explored.append(current_state.board)
        if current_state.board == SOLVED_STATE:
            solve_dto["solved_state"] = current_state
            solve_dto["explored_states"] = explored
            return solve_dto
        for valid_move in get_valid_moves(current_state.board):
            new_board = move(current_state.board, valid_move)
            if new_board in explored:
                continue
            idx = new_board.index(0)
            frontier.enqueue(State(new_board, idx, valid_move, current_state))
    return None

def solve_dfs(board):
    initial_state = State(board, board.index(0), None, None)
    solve_dto = {}
    explored = []
    frontier = Stack([initial_state])
    while frontier.data:
        current_state = frontier.pop()
        if current_state.board in explored:
            continue
        explored.append(current_state.board)
        if current_state.board == SOLVED_STATE:
            solve_dto["solved_state"] = current_state
            solve_dto["explored_states"] = explored
            return solve_dto
        for valid_move in get_valid_moves(current_state.board):
            new_board = move(current_state.board, valid_move)
            if new_board in explored:
                continue
            idx = new_board.index(0)
            frontier.push(State(new_board, idx, valid_move, current_state))
    return None

def get_path(solved_state):
    path = []
    current_state = solved_state["solved_state"]
    cost = current_state.cost
    while current_state.parent_state:
        if current_state.action: path.append(current_state.action.value)
        current_state = current_state.parent_state
    path.reverse()

    # Display solution
    print("")
    print("Path:", path)
    print("Cost:", cost)
    print("Explored States:", len(solved_state["explored_states"]))
    input("Press any key to continue.")
    print("")


def get_valid_moves(board):
    idx = board.index(0)
    valid_moves = [Moves.UP, Moves.DOWN, Moves.RIGHT, Moves.LEFT]
    if idx in [0,1,2]: valid_moves.remove(Moves.UP) # Top 3
    if idx in [2,5,8]: valid_moves.remove(Moves.RIGHT) # Right 3
    if idx in [6,7,8]: valid_moves.remove(Moves.DOWN) # Bottom 3
    if idx in [0,3,6]: valid_moves.remove(Moves.LEFT) # Left 3
    return valid_moves

def move(current_board, move):
    idx = current_board.index(0)
    board = list(current_board)
    if move == Moves.UP:
        if idx in [0,1,2]: # Top 3
            print("Invalid move! Undoing")
            return board
        else:
            board[idx],board[idx-3]=board[idx-3],board[idx]
            return board
    
    if move == Moves.DOWN:
        if idx in [6,7,8]: # Bottom 3
            print("Invalid move! Undoing")
            return board
        else:
            board[idx],board[idx+3]=board[idx+3],board[idx]
            return board

    if move == Moves.RIGHT:
        if idx in [2,5,8]: # Right 3
            print("Invalid move! Undoing")
            return board
        else:
            board[idx],board[idx+1]=board[idx+1],board[idx]
            return board

    if move == Moves.LEFT:
        if idx in [0,3,6]: # Left 3
            print("Invalid move! Undoing")
            return board
        else:
            board[idx],board[idx-1]=board[idx-1],board[idx]
            return board

def main():
    board = []
    getBoard(board, "puzzle.txt")
    if not is_solvable(board):
        print("WARNING: This puzzle is unsolvable!\n")
    print("8-Puzzle Game Solver:")
    print_board(board)

    solve_method = input("Choose how to solve this board:\n[1] Breadth First Search\n[2] Depth First Search\n[3] A* Search Algorithm\nEnter your choice: ")
    if solve_method == "1":
        solved_state: State = solve_bfs(board)
    elif solve_method == "2":
        solved_state: State = solve_dfs(board)
    elif solve_method == "3":
        heuristic = input("Choose a heuristic:\n[1] Misplaced Tiles\n[2] Manhattan Distance\n[3] Non-adjacent Tiles\nEnter your choice: ")
        if heuristic == "1":
            solved_state: State = solve_astar(board, Heuristics.H1)
        elif heuristic == "2":
            solved_state: State = solve_astar(board, Heuristics.H2)
        elif heuristic == "3":
            solved_state: State = solve_astar(board, Heuristics.H3)
        else:
            print("Invalid option!")
            return
    else:
        print("Invalid option!")
        return
                
    get_path(solved_state)
    return

# while True:
#     main()
    
