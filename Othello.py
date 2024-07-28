import tkinter as tk


class Gui:
    def __init__(self, root):

        self.root = root
        self.root.title("Othello Game")
        # building the board before anyone's turn
        self.size_of_cell = 100
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        # first screen to view options and make the player choose the level of difficulty
        self.difficulty = tk.StringVar(value="easy")  # easy is the default
        self.create_difficulty_options()
        # make the background purple
        self.canvas = tk.Canvas(self.root, width=8 * self.size_of_cell, height=8 * self.size_of_cell, bg='purple')
        self.canvas.pack()
        # make the player play first
        self.current_player = 'B'

    def create_difficulty_options(self):
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack()
        # building button to make the player choose between the levels and store a value when on clicking on a button
        tk.Label(self.options_frame, text="Select Difficulty: ").pack(side=tk.LEFT)
        tk.Radiobutton(self.options_frame, text="Easy", variable=self.difficulty, value="easy").pack(side=tk.LEFT)
        tk.Radiobutton(self.options_frame, text="Medium", variable=self.difficulty, value="medium").pack(side=tk.LEFT)
        tk.Radiobutton(self.options_frame, text="Hard", variable=self.difficulty, value="hard").pack(side=tk.LEFT)
        # build start game button
        start_button = tk.Button(self.options_frame, text="Start Game", command=self.start_game)
        start_button.pack(side=tk.LEFT)

    # function to remove options frame and draw the board
    def start_game(self):
        self.options_frame.destroy()
        self.draw_board()
        self.update_scores()
        self.canvas.bind("<Button-1>", self.on_click)

    # function to assign a value to  the depth based on difficulty
    def get_depth(self):
        difficulty = self.difficulty.get()
        if difficulty == "easy":
            return 1
        elif difficulty == "medium":
            return 3
        elif difficulty == "hard":
            return 5

    def draw_board(self):
        self.canvas.delete("disc")
        for i in range(8):
            for j in range(8):
                x0, y0 = j * self.size_of_cell, i * self.size_of_cell
                x1, y1 = x0 + self.size_of_cell, y0 + self.size_of_cell
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="purple", outline="black")
                if self.board[i][j] == 'B':
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="black", tags="disc")
                elif self.board[i][j] == 'W':
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="white", tags="disc")
        # put valid moves of the player to a list to create gery oval  to show valid moves of the player
        valid_moves = self.get_valid_moves('B')
        for move in valid_moves:
            r, c = move
            x0, y0 = c * self.size_of_cell, r * self.size_of_cell
            x1, y1 = x0 + self.size_of_cell, y0 + self.size_of_cell
            self.canvas.create_oval(x0 + 20, y0 + 20, x1 - 20, y1 - 20, outline="grey", width=3)

    def update_scores(self):
        try:
            # Calculate the scores
            player_score = sum(row.count('B') for row in self.board)
            computer_score = sum(row.count('W') for row in self.board)
            player_B_score = self.evaluate_state('B')
            player_W_score = self.evaluate_state('W')
            # Get valid moves for both players
            valid_moves = self.get_valid_moves('B')
            computer_moves = self.get_valid_moves('W')
            score_text = f"(Black): {player_score}   ||  (White): {computer_score}"
            # Check if there are no valid moves left for both players
            if not valid_moves and not computer_moves:
                if player_score > computer_score:
                    score_text = f"Winner is -> (Black): {player_score}"
                elif player_score < computer_score:
                    score_text = f"Game Over! (White): {computer_score}"
                else:
                    score_text = "Game ended in a Draw!"

                score_text += f"  | (Black) Score: {player_B_score}  | (White) Score: {player_W_score}"

            # Update the window title with the score text
            self.root.title("Othello Game - " + score_text)

        except Exception as e:
            # Handle exceptions
            print(f"Error updating scores: {e}")
            self.root.title("Othello Game - Error in updating scores")

    def on_click(self, event):
        # check if its player turn
        if self.current_player == 'B':
            col = event.x // self.size_of_cell
            row = event.y // self.size_of_cell
            # check if the click is on valid move
            if self.is_valid_move(row, col, 'B'):
                self.make_move(row, col, 'B')
                self.draw_board()
                self.update_scores()
                # executing computer move after every player turn if computer has valid moves
                if self.get_valid_moves('W'):
                    self.current_player = 'W'
                    self.root.after(500, self.computer_move)
                    self.update_scores()

    # function to decide its a valid move or not
    def is_valid_move(self, row, col, player):
        # check if the cell is empty
        if self.board[row][col] != ' ':
            return False
        # determine the valid directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# is valid move  if the direction is valid and there is an opposite player beside this move
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == ('W' if player == 'B' else 'B'):
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == ('W' if player == 'B' else 'B'):
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                    return True
        return False

# function to make the new move
    def make_move(self, row, col, player, board=None):
        if board is None:
            board = self.board
        board[row][col] = player
        # determine the valid directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# same for loop in function is valid move to make correct move
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == ('W' if player == 'B' else 'B'):
                to_flip = []
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == ('W' if player == 'B' else 'B'):
                    # storing all valid moves
                    to_flip.append((r, c))
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    # check if the chosen move is a valid move by check if it exists in to flip list
                    for flip_row, flip_col in to_flip:
                        board[flip_row][flip_col] = player

    # function to get valid move for player or computer
    def get_valid_moves(self, player):
        valid_moves = []
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(r, c, player):
                    valid_moves.append((r, c))
        return valid_moves

    def is_game_over(self):
        return not any(self.get_valid_moves('B')) and not any(self.get_valid_moves('W'))

    def simulate_move(self, move, player, board):
        new_board = [row[:] for row in board]
        self.make_move(move[0], move[1], player, new_board)
        return new_board

    def evaluate_state(self, player):
        player_score = sum(row.count(player) for row in self.board)
        opponent_score = sum(row.count('B' if player == 'W' else 'W') for row in self.board)
        return player_score - opponent_score

    def alpha_beta_algorithm(self, board, depth, player, alpha, beta):
        if depth == 0 or len(self.get_valid_moves(player)) == 0:
            return None, self.evaluate_state(player)

        valid_moves = self.get_valid_moves(player)
        best_move = None
        if player == 'W':
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = self.simulate_move(move, player, board)
                _, _eval = self.alpha_beta_algorithm(new_board, depth - 1, 'B', alpha, beta)
                if _eval > max_eval:
                    max_eval = _eval
                    best_move = move
                alpha = max(alpha, _eval)
                if beta <= alpha:
                    break
            return best_move, max_eval

        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = self.simulate_move(move, player, board)
                _, _eval = self.alpha_beta_algorithm(new_board, depth - 1, 'W', alpha, beta)
                if _eval < min_eval:
                    min_eval = _eval
                    best_move = move
                beta = min(beta, _eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def computer_move(self):
        if self.current_player == 'W':
            valid_moves = self.get_valid_moves('W')
            if valid_moves:
                best_move, _ = self.alpha_beta_algorithm(self.board, self.get_depth(), 'W', -float('inf'), float('inf'))
                if best_move:
                    self.make_move(best_move[0], best_move[1], 'W')
                    self.draw_board()
                    self.update_scores()
                    if self.get_valid_moves('B'):
                        self.current_player = 'B'
                    elif self.is_game_over():
                        print("game over")
                    else:
                        self.root.after(500, self.computer_move)


def main():
    root = tk.Tk()  # Create the main window
    root.title("Othello Game")  # Set the title of the window
    game = Gui(root)  # Create an instance of the Gui
    root.mainloop()  # Start the GUI event loop


if __name__ == "__main__":
    main()