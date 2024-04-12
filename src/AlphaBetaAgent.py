from Othello import OthelloBoard
from Heuristic import dynamic_heuristic_evaluation_function
import time

# Class that runs an Alpha-Beta Pruning search over the possible moves
class AlphaBetaAgent:
    def __init__(self, timeLimit):
        self.name = f"Alpha Beta Agent ({timeLimit}s)"
        self.depth_sum = 0
        self.depth_num = 0
        self.timeLimit = timeLimit

    def make_move(self, board: OthelloBoard):
        self.startTime = time.time()
        bestMove = None
        depth = 1
        while depth < 10:
            _, nextBoard = self.minimax(board, depth, float('-inf'), float('inf'))
            if time.time() - self.startTime >= self.timeLimit:
                break
            if nextBoard:
                bestMove = nextBoard
            depth += 1
        self.depth_num += 1
        self.depth_sum += depth-1
        if bestMove is None:
            print(depth)
            print(self.name)
        return bestMove

    def minimax(self, board: OthelloBoard, depth, alpha, beta):
        if time.time() - self.startTime >= self.timeLimit:
            return 0, None
        if board.game_over:
            black, white = board.count_pieces()
            if black > white:
                return float("inf"), None
            elif black < white:
                return float("-inf"), None
            else:
                return 0, None
        if depth == 0:
            return dynamic_heuristic_evaluation_function(board.board), None
        
        if board.current_player == 1:
            max_eval = float('-inf')
            best_move = None
            for child in board.generate_children():
                eval, _ = self.minimax(child, depth - 1, alpha, beta)
                if eval >= max_eval:
                    max_eval = eval
                    best_move = child
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for child in board.generate_children():
                eval, _ = self.minimax(child, depth - 1, alpha, beta)
                if eval <= min_eval:
                    min_eval = eval
                    best_move = child
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
