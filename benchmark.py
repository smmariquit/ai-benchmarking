import fababeir_exer02 as fababeir
import mariquit_exer02 as mariquit
import subprocess
import pandas as pd
import time
import copy

puzzles = ["puzzle.txt", "puzzle01.txt", "puzzle02.txt", "puzzle03.txt"]

ITERATIONS = 10
n_puzzles = len(puzzles)

fababeir_bfs_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])
fababeir_dfs_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])
fababeir_astar_manhattan_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])
fababeir_astar_misplaced_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])

mariquit_bfs_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])
mariquit_dfs_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])
mariquit_astar_manhattan_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])
mariquit_astar_misplaced_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])

# Benchmarking function for two implementations
def benchmark_both(func1, func2, puzzle_file):
    # Reset global state before each run
    fababeir.frontStack.clear()
    fababeir.exploredBoards.clear()
    
    # Create a fresh board for Fababeir (3x3 format)
    fresh_board_fababeir = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    fababeir.getBoard(fresh_board_fababeir, puzzle_file)

    # Create a fresh board for Mariquit (1D format)
    fresh_board_mariquit = []
    mariquit.getBoard(fresh_board_mariquit, puzzle_file)
    
    # Time fababeir implementation
    start = time.perf_counter()
    result1 = func1(fresh_board_fababeir)
    end = time.perf_counter()
    time_taken_fababeir = end - start
    print(f"Fababeir time: {time_taken_fababeir:0.7f} seconds")

    # Time mariquit implementation
    start = time.perf_counter()
    result2 = func2(fresh_board_mariquit)
    end = time.perf_counter()
    time_taken_mariquit = end - start
    print(f"Mariquit time: {time_taken_mariquit:0.7f} seconds")
    
    return time_taken_fababeir, time_taken_mariquit, result1, result2

# Single implementation benchmark function (for A* with heuristics, since the heuristic is passed as an argument)
def benchmark_single(func, board, *args):
    start = time.perf_counter()
    result = func(board, *args)
    end = time.perf_counter()
    time_taken = end - start
    print(f"Time taken: {time_taken:0.7f} seconds")
    return time_taken, result

print("Running BFS Benchmarks...")
for puzzle_idx, puzzle in enumerate(puzzles):
    print(f"\nTesting puzzle: {puzzle}")
    times_mariquit = []
    times_fababeir = []
    for i in range(ITERATIONS):
        print(f"Running {puzzle}, BFS Iteration {i+1}")
        try:
            time_taken_fababeir, time_taken_mariquit, result1, result2 = benchmark_both(fababeir.BFSearch, mariquit.solve_bfs, puzzle)
            times_mariquit.append(round(time_taken_mariquit*1000, 2))
            times_fababeir.append(round(time_taken_fababeir*1000, 2))
        except KeyboardInterrupt:
            print(f"Iteration {i+1} interrupted - likely taking too long")
            break
        except Exception as e:
            print(f"Error in iteration {i+1}: {e}")
            break
    
    if times_mariquit:
        average_time = f"{sum(times_mariquit) / len(times_mariquit):.2f}"
        formatted_times = [f"{t:.2f}" for t in times_mariquit]
        mariquit_bfs_performance.loc[len(mariquit_bfs_performance)] = [puzzle_idx] + formatted_times + ["0.00"] * (ITERATIONS - len(times_mariquit)) + [average_time]
    
    if times_fababeir:
        average_time = f"{sum(times_fababeir) / len(times_fababeir):.2f}"
        formatted_times = [f"{t:.2f}" for t in times_fababeir]
        fababeir_bfs_performance.loc[len(fababeir_bfs_performance)] = [puzzle_idx] + formatted_times + ["0.00"] * (ITERATIONS - len(times_fababeir)) + [average_time]


print("\nBFS Performance Results (Fababeir):")
print(fababeir_bfs_performance)

print("\nBFS Performance Results (Mariquit):")
print(mariquit_bfs_performance)

print("\nRunning DFS Benchmarks...")
for puzzle_idx, puzzle in enumerate(puzzles):
    print(f"\nTesting puzzle: {puzzle}")
    times_mariquit = []
    times_fababeir = []
    for i in range(ITERATIONS):
        print(f"Running {puzzle}, DFS Iteration {i+1}")
        try:
            time_taken_fababeir, time_taken_mariquit, result1, result2 = benchmark_both(fababeir.DFSearch, mariquit.solve_dfs, puzzle)
            times_mariquit.append(round(time_taken_mariquit*1000, 2))
            times_fababeir.append(round(time_taken_fababeir*1000, 2))
        except KeyboardInterrupt:
            print(f"Iteration {i+1} interrupted - likely taking too long")
            break
        except Exception as e:
            print(f"Error in iteration {i+1}: {e}")
            break
    
    if times_mariquit:
        average_time = f"{sum(times_mariquit) / len(times_mariquit):.2f}"
        formatted_times = [f"{t:.2f}" for t in times_mariquit]
        mariquit_dfs_performance.loc[len(mariquit_dfs_performance)] = [puzzle_idx] + formatted_times + ["0.00"] * (ITERATIONS - len(times_mariquit)) + [average_time]
    
    if times_fababeir:
        average_time = f"{sum(times_fababeir) / len(times_fababeir):.2f}"
        formatted_times = [f"{t:.2f}" for t in times_fababeir]
        fababeir_dfs_performance.loc[len(fababeir_dfs_performance)] = [puzzle_idx] + formatted_times + ["0.00"] * (ITERATIONS - len(times_fababeir)) + [average_time]

print("\nDFS Performance Results (Fababeir):")
print(fababeir_dfs_performance)

print("\nDFS Performance Results (Mariquit):")
print(mariquit_dfs_performance)

print("\nRunning A* Manhattan Benchmarks...")
for puzzle_idx, puzzle in enumerate(puzzles):
    print(f"\nTesting puzzle: {puzzle}")
    times_mariquit = []
    times_fababeir = []
    for i in range(ITERATIONS):
        print(f"Running {puzzle}, A* Manhattan Iteration {i+1}")
        try:
            # Reset global state before each run
            fababeir.frontStack.clear()
            fababeir.exploredBoards.clear()
            
            # Create a fresh board for Fababeir
            fresh_board_fababeir = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
            fababeir.getBoard(fresh_board_fababeir, puzzle)
            
            # Create a fresh board for Mariquit
            fresh_board_mariquit = []
            mariquit.getBoard(fresh_board_mariquit, puzzle)
            
            # Benchmark Fababeir
            time_taken_fababeir, result1 = benchmark_single(fababeir.solve_astar, fresh_board_fababeir, '2')  # Manhattan heuristic
            times_fababeir.append(round(time_taken_fababeir*1000, 2))
            
            # Benchmark Mariquit
            time_taken_mariquit, result2 = benchmark_single(mariquit.solve_astar, fresh_board_mariquit, mariquit.Heuristics.H2)  # Manhattan heuristic
            times_mariquit.append(round(time_taken_mariquit*1000, 2))
            
        except KeyboardInterrupt:
            print(f"Iteration {i+1} interrupted - likely taking too long")
            break
        except Exception as e:
            print(f"Error in iteration {i+1}: {e}")
            break
    
    if times_mariquit:
        average_time = f"{sum(times_mariquit) / len(times_mariquit):.2f}"
        formatted_times = [f"{t:.2f}" for t in times_mariquit]
        mariquit_astar_manhattan_performance.loc[len(mariquit_astar_manhattan_performance)] = [puzzle_idx] + formatted_times + ["0.00"] * (ITERATIONS - len(times_mariquit)) + [average_time]
    
    if times_fababeir:
        average_time = f"{sum(times_fababeir) / len(times_fababeir):.2f}"
        formatted_times = [f"{t:.2f}" for t in times_fababeir]
        fababeir_astar_manhattan_performance.loc[len(fababeir_astar_manhattan_performance)] = [puzzle_idx] + formatted_times + ["0.00"] * (ITERATIONS - len(times_fababeir)) + [average_time]

print("\nA* Manhattan Performance Results (Fababeir):")
print(fababeir_astar_manhattan_performance)

print("\nA* Manhattan Performance Results (Mariquit):")
print(mariquit_astar_manhattan_performance)

print("\nRunning A* Misplaced Benchmarks...")
for puzzle_idx, puzzle in enumerate(puzzles):
    print(f"\nTesting puzzle: {puzzle}")
    times_mariquit = []
    times_fababeir = []
    for i in range(ITERATIONS):
        print(f"Running {puzzle}, A* Misplaced Iteration {i+1}")
        try:
            # Reset global state before each run
            fababeir.frontStack.clear()
            fababeir.exploredBoards.clear()
            
            # Create a fresh board for Fababeir
            fresh_board_fababeir = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
            fababeir.getBoard(fresh_board_fababeir, puzzle)
            
            # Create a fresh board for Mariquit
            fresh_board_mariquit = []
            mariquit.getBoard(fresh_board_mariquit, puzzle)
            
            # Benchmark Fababeir
            time_taken_fababeir, result1 = benchmark_single(fababeir.solve_astar, fresh_board_fababeir, '1')  # Misplaced tiles heuristic
            times_fababeir.append(round(time_taken_fababeir*1000, 2))
            
            # Benchmark Mariquit
            time_taken_mariquit, result2 = benchmark_single(mariquit.solve_astar, fresh_board_mariquit, mariquit.Heuristics.H1)  # Misplaced tiles heuristic
            times_mariquit.append(round(time_taken_mariquit*1000, 2))
            
        except KeyboardInterrupt:
            print(f"Iteration {i+1} interrupted - likely taking too long")
            break
        except Exception as e:
            print(f"Error in iteration {i+1}: {e}")
            break
    
    if times_mariquit:
        average_time = f"{sum(times_mariquit) / len(times_mariquit):.2f}"
        formatted_times = [f"{t:.2f}" for t in times_mariquit]
        mariquit_astar_misplaced_performance.loc[len(mariquit_astar_misplaced_performance)] = [puzzle_idx] + formatted_times + ["0.00"] * (ITERATIONS - len(times_mariquit)) + [average_time]
    
    if times_fababeir:
        average_time = f"{sum(times_fababeir) / len(times_fababeir):.2f}"
        formatted_times = [f"{t:.2f}" for t in times_fababeir]
        fababeir_astar_misplaced_performance.loc[len(fababeir_astar_misplaced_performance)] = [puzzle_idx] + formatted_times + ["0.00"] * (ITERATIONS - len(times_fababeir)) + [average_time]

print("\nA* Misplaced Performance Results (Fababeir):")
print(fababeir_astar_misplaced_performance)

print("\nA* Misplaced Performance Results (Mariquit):")
print(mariquit_astar_misplaced_performance)

import subprocess

fababeir_minimax_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])
mariquit_minimax_performance = pd.DataFrame(columns=["Case #"] + [str(i) for i in range(1, ITERATIONS + 1)] + ["Average"])

times_mariquit_minimax = []
times_fababeir_minimax = []

for i in range(ITERATIONS):
    print(f"\nRunning Mariquit Minimax Iteration {i+1}")
    start = time.perf_counter()
    result = subprocess.run(['python', 'mariquit_exer03.py'], 
                           input="1\n2 2\n1 3\n2 1\n3 3\n",
                           text=True)
    end = time.perf_counter()
    mariquit_time = end - start
    print(f"Mariquit Minimax time: {mariquit_time:0.7f} seconds")
    
    print(f"\nRunning Fababeir Minimax Iteration {i+1}")
    start = time.perf_counter()
    result = subprocess.run(['python', 'fababeir_exer03.py'], 
                           input="2\n5\n3\n4\n9\n", 
                           text=True)
    end = time.perf_counter()
    fababeir_time = end - start
    print(f"Fababeir Minimax time: {fababeir_time:0.7f} seconds")

    times_mariquit_minimax.append(round(mariquit_time*1000, 2))
    times_fababeir_minimax.append(round(fababeir_time*1000, 2))

# Format minimax data properly
if times_mariquit_minimax:
    average_time_mariquit = f"{sum(times_mariquit_minimax) / len(times_mariquit_minimax):.2f}"
    formatted_times_mariquit = [f"{t:.2f}" for t in times_mariquit_minimax]
    mariquit_minimax_performance.loc[0] = [0] + formatted_times_mariquit + ["0.00"] * (ITERATIONS - len(times_mariquit_minimax)) + [average_time_mariquit]

if times_fababeir_minimax:
    average_time_fababeir = f"{sum(times_fababeir_minimax) / len(times_fababeir_minimax):.2f}"
    formatted_times_fababeir = [f"{t:.2f}" for t in times_fababeir_minimax]
    fababeir_minimax_performance.loc[0] = [0] + formatted_times_fababeir + ["0.00"] * (ITERATIONS - len(times_fababeir_minimax)) + [average_time_fababeir]

print("\nMinimax Performance Results (Fababeir):")
print(fababeir_minimax_performance)
print(f"Average time (Fababeir): {average_time_fababeir} ms")

print("\nMinimax Performance Results (Mariquit):")
print(mariquit_minimax_performance)
print(f"Average time (Mariquit): {average_time_mariquit} ms")

# index=False so that the row index isnt written on the left
mariquit_minimax_performance.to_csv("mariquit_minimax_performance.csv", index=False)
fababeir_minimax_performance.to_csv("fababeir_minimax_performance.csv", index=False)
mariquit_bfs_performance.to_csv("mariquit_bfs_performance.csv", index=False)
fababeir_bfs_performance.to_csv("fababeir_bfs_performance.csv", index=False)
mariquit_dfs_performance.to_csv("mariquit_dfs_performance.csv", index=False)
fababeir_dfs_performance.to_csv("fababeir_dfs_performance.csv", index=False)
mariquit_astar_manhattan_performance.to_csv("mariquit_astar_manhattan_performance.csv", index=False)
fababeir_astar_manhattan_performance.to_csv("fababeir_astar_manhattan_performance.csv", index=False)
mariquit_astar_misplaced_performance.to_csv("mariquit_astar_misplaced_performance.csv", index=False)
fababeir_astar_misplaced_performance.to_csv("fababeir_astar_misplaced_performance.csv", index=False)    