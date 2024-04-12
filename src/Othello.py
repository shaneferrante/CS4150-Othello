class OthelloBoard:
    def __init__(self, other=None):
        if other is None:
            # Initialize the board with empty squares
            self.board = [[0] * 8 for _ in range(8)]
            # Initial black and white pieces
            self.board[3][3] = self.board[4][4] = 1
            self.board[3][4] = self.board[4][3] = -1
            self.current_player = 1  # 1 for black, -1 for white
            self.game_over = False
        else:
            # Copy attributes from the other instance
            self.board = [row[:] for row in other.board]
            self.current_player = other.current_player
            self.game_over = other.game_over

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.flip_pieces(row, col)
            self.current_player = -self.current_player
            if not self.has_valid_move():
                self.current_player = -self.current_player  # Switch back to the original player
                if not self.has_valid_move():  # If both players have no valid moves
                    self.game_over = True
        else:
            print("Invalid move")

    def is_valid_move(self, row, col):
        if self.board[row][col] != 0:
            return False
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self.is_valid_direction(row, col, dr, dc):
                    return True
        return False

    def is_valid_direction(self, row, col, dr, dc):
        opponent = -self.current_player
        r, c = row + dr, col + dc
        if not (0 <= r < 8 and 0 <= c < 8):
            return False
        if self.board[r][c] != opponent:
            return False
        r, c = r + dr, c + dc
        while 0 <= r < 8 and 0 <= c < 8:
            if self.board[r][c] == 0:
                return False
            if self.board[r][c] == self.current_player:
                return True
            r, c = r + dr, c + dc
        return False

    def flip_pieces(self, row, col):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self.is_valid_direction(row, col, dr, dc):
                    self.flip_direction(row, col, dr, dc)

    def flip_direction(self, row, col, dr, dc):
        opponent = -self.current_player
        r, c = row + dr, col + dc
        while self.board[r][c] == opponent:
            self.board[r][c] = self.current_player
            r, c = r + dr, c + dc

    def has_valid_move(self):
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    return True
        return False

    def count_pieces(self):
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(-1) for row in self.board)
        return black_count, white_count
    
    def get_result(self):
        black, white = self.count_pieces()
        if black == white:
            return 0
        return 1 if black > white else -1

    def display(self):
        for row in self.board:
            print(row)
    
    def generate_children(self):
        children = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    child_board = OthelloBoard(self)  # Create a copy of the current board
                    child_board.make_move(row, col)  # Make the move on the child board
                    children.append(child_board)
        return children
