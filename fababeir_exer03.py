# Responsible Use of AI
# Asked AI how pruning affects the search for the best possible move

import random

board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
currentPlayer = "X"
winner = None
gameLoop = True
moveCounter = 1

# Print Board
def printBoard(board):
    print(board[0] + " | " + board[1] + " | " + board[2])
    print(board[3] + " | " + board[4] + " | " + board[5])
    print(board[6] + " | " + board[7] + " | " + board[8])
    print("\n")

# Get Input
def getPlayerInput(board):
    while True:
        playerInput = int(input(f"Choose a Slot (1-9): "))
        if playerInput >= 1 and playerInput <= 9 and board[playerInput-1] == "-":
            board[playerInput-1] = "X"
            return True
        else:
            print("Invalid Action!")
            
# Get AI Input
def getAIInput(board):
    bestScore = float('-inf')
    bestMove = -1
    
    alpha = float('-inf')
    beta = float('inf')
    
    for i in range(9): # Solves for the score of all possible moves
        if board[i] == "-":
            board[i] = "O"
            score = minimax(board, 0, False, alpha, beta)
            board[i] = "-" # Reset Board
            
            if score > bestScore:
                bestScore = score
                bestMove = i
            
            alpha = max(alpha, bestScore)
                
    board[bestMove] = "O"

def minimax(board, depth, maximizing, alpha, beta):
    result = checkWinCondition(board)
    if result is not None:
        if result == "X":
            return -1
        elif result == "O":
            return 1
        else:
            return 0
        
    if maximizing: 
        bestScore = float('-inf')
        for i in range(9): # Solves for the score of all possible moves
            if board[i] == "-":
                board[i] = "O"
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = "-" # Reset Board
                bestScore = max(score, bestScore)

                alpha = max(alpha, bestScore)
                if beta <= alpha:
                    break

        return bestScore
    
    else: # Minimizing Player
        bestScore = float('inf')
        for i in range(9): # Solves for the score of all possible moves
            if board[i] == "-":
                board[i] = "X"
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = "-" # Reset Board
                bestScore = min(score, bestScore)

                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

        return bestScore	
                
# Swap Player
def swapPlayer(currentPlayer):
    if currentPlayer == "X":
        return "O"
    else:
        return "X"

# Win Condition
def checkWinCondition(board):
    #Horizontal Win Conditions
    if board[0] == board[1] == board[2] != "-":
        return board[0]
    if board[3] == board[4] == board[5] != "-":
        return board[3]
    if board[6] == board[7] == board[8] != "-":
        return board[6]
    
    #Vertical Win Conditions
    if board[0] == board[3] == board[6] != "-":
        return board[0]
    if board[1] == board[4] == board[7] != "-":
        return board[1]
    if board[2] == board[5] == board[8] != "-":
        return board[2]
    
    #Diagonal Win Conditions
    if board[0] == board[4] == board[8] != "-":
        return board[0]
    if board[2] == board[4] == board[6] != "-":
        return board[2]
    
    #Tie Condition 
    if "-" not in board:
        return "Tie!"

    return None	

# Main Loop


#while True:
board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
currentPlayer = "X"
gameLoop = True

moveChoice = int(input("Choose to Move First (1) or Move Second (2): "))
if moveChoice == 1:
    printBoard(board)
    while gameLoop:
        if currentPlayer == "X":
            getPlayerInput(board)
        else:
            getAIInput(board)
        printBoard(board)
        result = checkWinCondition(board)
        if result is not None:
            if result == "Tie!":
                print("Tie!")
            else:
                print(f"The winner is {result}")
            gameLoop = False
        else:
            currentPlayer = swapPlayer(currentPlayer)
elif moveChoice == 2:
    board[0] = "O"
    printBoard(board)
    while gameLoop:
        if currentPlayer == "X":
            getPlayerInput(board)
        else:
            getAIInput(board)
        printBoard(board)
        result = checkWinCondition(board)
        if result is not None:
            if result == "Tie!":
                print("Tie!")
            else:
                print(f"The winner is {result}")
            gameLoop = False
        else:
            currentPlayer = swapPlayer(currentPlayer)
else:
    print("Invalid ")