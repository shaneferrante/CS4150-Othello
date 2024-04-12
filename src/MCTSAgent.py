from Othello import OthelloBoard
from Heuristic import dynamic_heuristic_evaluation_function
import math
import random
import time

# Class to represent a node or board state
class Node:
    def __init__(self, state: OthelloBoard):
        self.state: OthelloBoard = state
        self.parent = None
        self.children = []
        self.visits = 0
        self.wins = 0

    def expand(self):
        for child in self.state.generate_children():
            child_node = Node(child)
            child_node.parent = self
            self.children.append(child_node)

    # Select a child using Upper Confidence Bound algorithm
    def select_child(self, lcb = False):
        selected_child = None
        best_ucb = -math.inf
        for child in self.children:
            if child.visits == 0:
                return child
            winrate = (child.wins/child.visits) if child.state.current_player == self.state.current_player else (1 - child.wins/child.visits)
            ucb = winrate + math.sqrt(2 * math.log(self.visits) / child.visits) * (-1 if lcb else 1)
            if ucb > best_ucb:
                best_ucb = ucb
                selected_child = child
        return selected_child

    def update(self, result):
        self.visits += 1
        if result == self.state.current_player:
            self.wins += 1
        elif result == 0:
            self.wins += 0.5
        if self.parent:
            self.parent.update(result)

    def display(self, indent = 0):
        print(f'{" "*indent}Visits:{self.visits}')
        print(f'{" "*indent}Wins:{self.wins}')
        print(f'{" "*indent}To Move:{self.state.current_player}')
        print(f'{" "*indent}Children({len(self.children)}): [')
        for child in self.children:
            child.display(indent+4)
        print(f"{" "*indent}]")

# Agent that selects a node using MCTS
class MonteCarloTreeSearchAgent:
    def __init__(self, timeLimit):
        self.root = None
        self.name = f"MCTS Agent ({timeLimit}s)"
        self.visits_num = 0
        self.visits_sum = 0
        self.timeLimit = timeLimit

    def make_move(self, board: OthelloBoard):
        self.root = Node(board)
        counts = board.count_pieces()
        pieces = counts[0]+counts[1]
        self.search(self.timeLimit*(64-pieces)/30)
        best_move = self.root.select_child(lcb=True)
        #print("Root")
        #self.root.display()
        #print("Best Move")
        #best_move.display()
        self.visits_num += 1
        self.visits_sum += self.root.visits
        return best_move.state

    def search(self, timeLimit):
        start = time.time()
        iteration = 1
        while iteration < 1000:
            if time.time() - start >= timeLimit:
                break
            #print(f'iteration: {i}')
            #self.root.display()
            node = self.select_node()
            result = self.simulate(node.state)
            node.update(result)
            iteration += 1

    def select_node(self):
        node = self.root
        while node.children:
            node = node.select_child()
        if node.state.game_over:
            return node
        if node.visits == 0:
            node.expand()
            return random.choice(node.children)
        return node

    def simulate(self, state: OthelloBoard):
        # Perform random playouts until the game ends
        while not state.game_over:
            best_move = None
            if state.current_player == 1:
                best_heuristic = float("-inf")
                for move in state.generate_children():
                    hr = dynamic_heuristic_evaluation_function(move.board)
                    if hr > best_heuristic:
                        best_heuristic = hr
                        best_move = move
            else:
                best_heuristic = float("inf")
                for move in state.generate_children():
                    hr = dynamic_heuristic_evaluation_function(move.board)
                    if hr < best_heuristic:
                        best_heuristic = hr
                        best_move = move
            
            state = best_move
        return state.get_result()  # Return the result of the simulated game
