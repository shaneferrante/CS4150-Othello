import pygame
import sys

from Othello import OthelloBoard
from AlphaBetaAgent import AlphaBetaAgent
from MCTSAgent import MonteCarloTreeSearchAgent

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 600
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
DISPLAY_MOVES = True

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

# Function to draw the game board
def draw_board(board : OthelloBoard):
    screen.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
            if board.board[row][col] != 0:
                pygame.draw.circle(screen, BLACK if board.board[row][col] == 1 else WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 30)
            if board.is_valid_move(row, col):
                pygame.draw.circle(screen, BLACK if board.current_player == 1 else WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

# Function to get row and column from mouse click position
def get_row_col_from_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Main function to run the game
def main():
    running = True
    board = OthelloBoard()
    alphaAgent = AlphaBetaAgent(1)
    while running:
        if not board.game_over:
            if board.current_player == -1:
                board = alphaAgent.make_move(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_pos(pos)
                    board.make_move(row, col)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #board = agent.make_move(board)
                    pass
                if event.key == pygame.K_r:
                    board = OthelloBoard()
        
        draw_board(board)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
