import re
import copy # Copy is used for deepcopy, for an actual copy not just referencing. https://stackoverflow.com/questions/19210971/python-prevent-copying-object-as-reference
import heapq

board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
rowIndex = None
colIndex = None
frontStack = []
exploredBoards = []

def getBoard(board, puzzle):
	with open(puzzle, "r") as file:
		data = file.read()

		numbers = re.findall(r'\d+', data)
		# print(numbers)

	fileInputIndex = 0
	for row in range(3):
		for col in range(3):
			board[row][col] = numbers[fileInputIndex]
			fileInputIndex = fileInputIndex + 1

# Print Board
def printBoard(inputboard):
	print(inputboard[0][0] + " | " + inputboard[0][1] + " | " + inputboard[0][2])
	print(inputboard[1][0] + " | " + inputboard[1][1] + " | " + inputboard[1][2])
	print(inputboard[2][0] + " | " + inputboard[2][1] + " | " + inputboard[2][2])

# Get Input
def getPlayerInput(board):
	playerInput = input("Move Direction (w/a/s/d | W/A/S/D): ")
	executeMove(board, playerInput)

# Get Location of 0
def getLoc(board):
	for row, col in enumerate(board): # Iterates the 2D Array
		if "0" in col:
			rowIndex = row
			colIndex = col.index("0")
			break
	return rowIndex, colIndex

# Get Valid Moves
def executeMove(board, playerInput):
	# Up
	if playerInput == "w" or playerInput == "W":
		if rowIndex-1 >= 0: # Check if up is in bounds, then swap numbers
			temp = "0"
			board[rowIndex][colIndex] = board[rowIndex-1][colIndex]
			board[rowIndex-1][colIndex] = temp

	# Left
	if playerInput == "a" or playerInput == "A":
		if colIndex-1 >= 0: # Check if left is in bounds, then swap numbers
			temp = "0"
			board[rowIndex][colIndex] = board[rowIndex][colIndex-1]
			board[rowIndex][colIndex-1] = temp

	# Down
	if playerInput == "s" or playerInput == "S":
		if rowIndex+1 <= 2: # Check if down is in bounds, then swap numbers
			temp = "0"
			board[rowIndex][colIndex] = board[rowIndex+1][colIndex]
			board[rowIndex+1][colIndex] = temp

	# Right
	if playerInput == "d" or playerInput == "D":
		if colIndex+1 <= 2: # Check if right is in bounds, then swap numbers
			temp = "0"
			board[rowIndex][colIndex] = board[rowIndex][colIndex+1]
			board[rowIndex][colIndex+1] = temp

# Win Condition
def checkWinCondition(board):
	return board == [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "0"]]
	# Simplified
	
# Print Possible Moves
def getPossibleMoves(board):
	if isinstance(board, tuple):
		board = [list(row) for row in board]

	rowIndex, colIndex = getLoc(board)
	possibleMoves = []
	
	boardDuplicateUp = copy.deepcopy(board)
	boardDuplicateLeft = copy.deepcopy(board)
	boardDuplicateDown = copy.deepcopy(board)
	boardDuplicateRight = copy.deepcopy(board)
	
	if rowIndex-1 >= 0: # Check if up is in bounds, then swap numbers
		temp1 = "0"
		boardDuplicateUp[rowIndex][colIndex] = boardDuplicateUp[rowIndex-1][colIndex]
		boardDuplicateUp[rowIndex-1][colIndex] = temp1
		#printBoard(boardDuplicateUp)
		possibleMoves.append((boardDuplicateUp, "U"))
		
	if rowIndex+1 <= 2: # Check if down is in bounds, then swap numbers
		temp3= "0"
		boardDuplicateDown[rowIndex][colIndex] = boardDuplicateDown[rowIndex+1][colIndex]
		boardDuplicateDown[rowIndex+1][colIndex] = temp3
		#printBoard(boardDuplicateDown)
		possibleMoves.append((boardDuplicateDown, "D"))
		
	if colIndex+1 <= 2: # Check if right is in bounds, then swap numbers
		temp4 = "0"
		boardDuplicateRight[rowIndex][colIndex] = boardDuplicateRight[rowIndex][colIndex+1]
		boardDuplicateRight[rowIndex][colIndex+1] = temp4
		#printBoard(boardDuplicateRight)
		possibleMoves.append((boardDuplicateRight, "R"))
	
	if colIndex-1 >= 0: # Check if left is in bounds, then swap numbers
		temp2 = "0"
		boardDuplicateLeft[rowIndex][colIndex] = boardDuplicateLeft[rowIndex][colIndex-1]
		boardDuplicateLeft[rowIndex][colIndex-1] = temp2
		#printBoard(boardDuplicateLeft)
		possibleMoves.append((boardDuplicateLeft, "L"))

	# print(possibleMoves)
	return possibleMoves

# Stores the board to be explored
def frontierStack(board, action, parent):
	frontStack.append({
		"puzzle": board,
		"action": action,
		"parent": parent, 
    })

# For the Move Path and Cost
def getSolutionPath(state):
	solutionPath = []
	solutionString = ""
	while state and state['parent'] is not None:
		solutionPath.append(state['action'])
		state = state['parent']
	
	solutionPath.reverse()
	solutionCost = len(solutionPath)

	for action in solutionPath:
		# print(f"Move: {action}")
		solutionString = solutionString + " " + action
	print(f"Solution Path:{solutionString}")
	print(f"Solution Cost: {solutionCost}")

def misplaced_tiles(board):
	count = 0
	misplaced_tiles = 0
	for i in range(3):
		for j in range(3):
			count = count + 1
			tile = board[i][j]
			if int(tile) != int(count) and tile != 0:
				misplaced_tiles = misplaced_tiles + 1
	return misplaced_tiles

def manhattan_distance(board):
	distance = 0
	for i in range(3):
		for j in range(3):
			tile = board[i][j]
			if tile != "0":
				current_i = (int(tile) - 1) // 3 
				current_j = (int(tile) - 1) % 3
				distance = distance + (abs(i - current_i) + abs(j - current_j))
	return distance

# BFS
def BFSearch(board):
	frontierStack(board, "", None) #Initiates the board first, without any actions and parents
	exploredBoards = []

	while frontStack:
		currentState = frontStack.pop(0) # Pops the head of the list
		currentBoard = currentState['puzzle']

		if currentBoard in exploredBoards:
			continue

		exploredBoards.append(currentBoard)

		if checkWinCondition(currentBoard):
			print("\n")
			print(f"Explored Boards: {len(exploredBoards)}")
			getSolutionPath(currentState)
			return currentState
		
		possibleMoves = getPossibleMoves(currentBoard)
		for moves, action in possibleMoves:
			frontierStack(moves, action, currentState)

# DFS
def DFSearch(board):
	frontierStack(board, "", None) #Initiates the board first, without any actions and parents
	exploredBoards = []

	while frontStack:
		currentState = frontStack.pop() # Pops the tail of the list
		currentBoard = currentState['puzzle']

		if currentBoard in exploredBoards:
			continue

		exploredBoards.append(currentBoard)

		if checkWinCondition(currentBoard):
			print(f"Explored Boards: {len(exploredBoards)}")
			getSolutionPath(currentState)
			return currentState
		
		possibleMoves = getPossibleMoves(currentBoard)
		for moves, action in possibleMoves:
			frontierStack(moves, action, currentState)
			
def solve_astar(board, heuristic):
	frontierList = [] # Acts as the open list
	exploredBoards = {} # Acts as the closed list
	count = 0
	
	g_cost = 0
	if heuristic == '1':
		h_cost = misplaced_tiles(board)
	elif heuristic == '2':
		h_cost = manhattan_distance(board)
	elif heuristic == '3':
		return print("Not Implemented!")
	else:
		return print("Invalid")
	f_cost = g_cost + h_cost
	
	initial_state = {
		"puzzle": board,
		"action": "",
		"parent": None,
		"g_cost": g_cost
	}
	
	# Each push of heap is sorted by f_cost
	# For cases of f_cost tie, count will be used as a secondary comparison
	heapq.heappush(frontierList, (f_cost, count, initial_state))
	convertedBoard = (tuple(tuple(row) for row in board))

	while frontierList:
		f_cost, counter, currentState = heapq.heappop(frontierList)
		currentBoard = currentState['puzzle'] # Acts as the current best node
		
		convertedBoard = (tuple(tuple(row) for row in currentBoard))
		exploredBoards[convertedBoard] = f_cost

		if checkWinCondition(currentBoard):
			print(f"Explored Boards: {len(exploredBoards)}")
			getSolutionPath(currentState)
			return currentState
		
		possibleMoves = getPossibleMoves(currentBoard)
		for moves, action in possibleMoves:
			new_g_cost = currentState['g_cost'] + 1
			if heuristic == '1':
				new_h_cost = misplaced_tiles(moves)
			elif heuristic == '2':
				new_h_cost = manhattan_distance(moves)
			elif heuristic == '3':
				return print("Not Implemented!")
			else:
				return print("Invalid")
			new_f_cost = new_g_cost + new_h_cost
			
			new_board = (tuple(tuple(row) for row in moves))	
			
			if (new_board not in (exploredBoards)) or ((new_f_cost < exploredBoards[new_board])):
				new_state = {
					"puzzle": moves,
					"action": action,
					"parent": currentState,
					"g_cost": new_g_cost
				}
				
				count = count + 1
				heapq.heappush(frontierList, (new_f_cost, count, new_state))

# # Main Loop
# getBoard(board, puzzle="puzzle01.txt")

# while True:
# 	print("\nSelect Strategy:\n[1] - BFS\n[2] - DFS\n[3] - A*\n[4] - Exit")
# 	choice = input("Chioce: ")

# 	if choice == '1':
# 		solution = BFSearch(board)
# 		if solution:
# 			print("\nDone!")
# 		else:
# 			print("Solution Not Found")
# 	elif choice == '2':
# 		solution = DFSearch(board)
# 		if solution:
# 			print("\nDone!")
# 		else:
# 			print("Solution Not Found")
# 	elif choice == '3':
# 		print("\nSelect Heuristic Function:\n[1] - Misplaced Tiles\n[2] - Manhattan\n[3] - Non-Adjacent Tiles\n[4] - Exit")
# 		heuristic_choice = input("Chioce: ")
# 		solution = solve_astar(board, heuristic_choice)
# 		if solution:
# 			print("\nDone!")
# 		else:
# 			print("Solution Not Found")
# 	elif choice == '4':
# 		print("Goodbye World!")
# 		break
# 	else:
# 		print("Invalid")

