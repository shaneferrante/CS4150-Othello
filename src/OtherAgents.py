from Othello import OthelloBoard
import random

# Class of agents designed to play simply based on maximizing a board heuristic after a single move
class HeuristicAgent():
    def __init__(self, heuristic, name):
        self.heuristic = heuristic
        self.name = name

    def make_move(self, board: OthelloBoard):
        best_move = None
        best_val = float("-inf")
        for child in board.generate_children():
            val = self.heuristic(child, board.current_player)
            if val > best_val:
                best_move = child
                best_val = val
        return best_move
    
# Returns the number of stones for the current player
def max_stones_heuristic(board: OthelloBoard, current_player):
    return board.count_pieces()[0 if current_player == 1 else 1]

# Returns the number of the stones for the other player
def min_stones_heuristic(board: OthelloBoard, current_player):
    return board.count_pieces()[0 if current_player == -1 else 1]

# Complete randomness
def random_heuristic(board: OthelloBoard, current_player):
    return random.random()

MaxStonesAgent = HeuristicAgent(max_stones_heuristic, "Max Stones Agent")
MinStonesAgent = HeuristicAgent(min_stones_heuristic, "Min Stones Agent")
RandomAgent = HeuristicAgent(random_heuristic, "Random Agent")