# Build the board
# Chess is an 8x8 board, we can express this as a list of lists

# [ [], [], []...],
# [ [], [], []...],

# so we need to loop through to add each rank, and loop through each rank to add each file

from rules import Rules


def prYellow(s): 
    print("\033[93m{}\033[00m".format(s), end=" ")


def prBlue(s):
    print("\033[96m{}\033[00m".format(s), end=" ")


class Board:
    def __init__(self):
        self.ranks = 8
        self.files = 8

        self.board = self.initialise_board()
        self.insert_pieces()

        self.rules = Rules()

        self.taken_piece = []

        self.current_turn = "w"

    def initialise_board(self):
        board = []
        i = 0
        while i < self.ranks:
            board.append([])
            j = 0
            while j < self.files:
                board[i].append(None)
                j += 1
            i += 1

        # print("\n".join(str(row) for row in board))
        return board


    def insert_pieces(self) -> None:
        # we need to be able to distinguish between black and white pieces so we can preface with w / b. 
        # pieces will be denoted by p: pawn, r: rook, k: king, q: queen, b: bishop, kn: knight.
        # piece example: wk: white king, bp: black pawn. We don't need to care about which square they start on as their movement patterns restrict them.
        # because the back row is the same for white and black we can just insert the whole row for each.

        back_row = ["r", "kn", "b", "q", "k", "b", "kn", "r"]

        for column, piece in enumerate(back_row):
            self.board[0][column] = "b" + piece
            self.board[1][column] = "bp"
            self.board[6][column] = "wp"
            self.board[7][column] = "w" + piece


    def render_board(self, selected_square=None, highlighted_squares=None) -> None:
        print("\033[2J\033[H", end="", flush=True)

        if highlighted_squares is None:
            highlighted_squares = []

        if selected_square is None:
            selected_square = []

        for row_index, row in enumerate(self.board):
            for column_index, piece in enumerate(row):
                text = f"{piece if piece is not None else 'X':>3}"

                if (row_index, column_index) in highlighted_squares:
                    prYellow(text)

                elif (row_index, column_index) == selected_square:
                    prBlue(text)

                else:
                    print(text, end=" ")
            print()
        print(" ###############################")


    def move_piece(self, from_square, to_square) -> bool:
        piece = self.board[from_square[0]][from_square[1]]
        if piece is None or piece[0] != self.current_turn:
            print("Not your turn!")
            return False

        if not to_square in self.rules.possible_moves(self.board, from_square):
            return False

        if self.board[to_square[0]][to_square[1]] is not None:
            self.taken_pieces(self.board[to_square[0]][to_square[1]])

        self.board[to_square[0]][to_square[1]] = piece
        
        if self.current_turn == "w":
            self.current_turn = "b"

        else:
            self.current_turn = "w"

        self.render_board(selected_square=from_square)
        self.board[from_square[0]][from_square[1]] = None
        
        return True


    def select_piece(self, from_square) -> bool:
        # Updates board state to print possible moves, should come before move_piece
        # Select -> move
        piece = self.board[from_square[0]][from_square[1]]
        if piece is None or piece[0] != self.current_turn:
            return False

        moves = self.rules.possible_moves(self.board, from_square)
        self.render_board(selected_square=from_square, highlighted_squares=moves)

        return True        


    def taken_pieces(self, piece) -> None:
        self.taken_piece.append(piece)



if __name__ == "__main__":
    board = Board()
    board.render_board()

